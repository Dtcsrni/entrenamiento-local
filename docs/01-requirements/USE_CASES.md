# Casos de uso

## UC-TRN-001 — Registrar entrenamiento

**Actor:** usuario.
**Precondición:** existe una rutina o se inicia sesión vacía.

Flujo principal:

1. El usuario inicia la sesión.
2. El sistema muestra cardio inicial, fuerza y cardio final configurados.
3. El usuario completa series; cada una se guarda localmente.
4. El sistema inicia descanso y precarga el objetivo siguiente.
5. El usuario corrige o sustituye ejercicios cuando sea necesario.
6. El usuario revisa y finaliza.
7. El sistema calcula métricas versionadas y programa sincronización.

Alternativas:

- Sin red: la sesión continúa sin degradar el registro.
- Cierre del proceso: se reconstruye desde Room.
- Tezkatli ausente: analítica pesada queda pendiente.
- Máquina ocupada: se propone sustitución sin alterar el catálogo.

## UC-NUT-001 — Registrar plato por fotografía

1. El usuario selecciona captura rápida o precisa.
2. Se evalúa calidad de imagen localmente.
3. Se detecta si existe código, etiqueta o plato.
4. Se crea un trabajo remoto si es necesario.
5. Tezkatli ejecuta segmentación, identificación, geometría y normalización.
6. El teléfono recibe un borrador con componentes, cantidades y supuestos.
7. El usuario corrige y confirma.
8. Solo entonces se incorpora al diario.

Excepciones:

- El archivo no es una imagen válida.
- No existe conexión.
- El modelo no identifica componentes.
- La cantidad no puede estimarse con utilidad.
- La respuesta llega después de que el usuario confirmó manualmente.

## UC-NUT-002 — Registrar por texto

1. El usuario escribe o dicta una descripción.
2. El parser extrae alimentos, cantidades y unidades.
3. Se resuelven candidatos contra catálogos y memoria personal.
4. Las ambigüedades se muestran para corrección.
5. El usuario confirma.

## UC-SUP-001 — Confirmar suplemento

1. Se muestra recordatorio local.
2. El usuario confirma, pospone u omite.
3. Se registra el evento con la hora real.
4. Se actualiza inventario.
5. La IA no cambia la dosis programada.

## UC-GYM-001 — Llegada al gimnasio

1. Una geofence genera señal de entrada.
2. El sistema combina horario, movimiento y señales disponibles.
3. Tras histéresis, muestra una sugerencia.
4. El usuario confirma o descarta.
5. Solo una confirmación crea la sesión.

## UC-WEA-001 — Completar serie desde reloj

1. El reloj muestra la serie actual.
2. El usuario confirma resultado o ajusta un dato simple.
3. Se crea un evento durable con ID y secuencia.
4. Side Service intenta enviarlo.
5. Android/Tezkatli confirma recepción idempotente.
6. El reloj marca el evento como entregado.

Este caso de uso queda condicionado por SPIKE-001.

## UC-REC-001 — Restaurar datos

1. El usuario selecciona un respaldo cifrado compatible.
2. El sistema valida integridad, versión y espacio.
3. Restaura en una ubicación temporal.
4. Ejecuta migraciones y verificaciones.
5. Sustituye el almacenamiento activo de forma atómica.
6. Presenta un reporte de restauración.
