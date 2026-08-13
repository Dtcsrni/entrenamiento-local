# Runbook operativo

## Entornos

- `development`: fixtures sintéticos y modelos simulados.
- `integration`: Android + API/worker local.
- `release-candidate`: configuración equivalente a producción sin datos reales completos.
- `personal-production`: teléfono, reloj y Tezkatli reales.

## Inicio de Tezkatli

Procedimiento definitivo pendiente de SPIKE-003. Debe incluir:

1. Validar disco y base.
2. Iniciar red privada.
3. Iniciar API en interfaz restringida.
4. Iniciar worker con límite de concurrencia.
5. Consultar health/readiness.
6. Ejecutar trabajo sintético.

## Health checks

- API viva.
- Base legible/escribible.
- Cola sin corrupción.
- Espacio suficiente.
- Runtime de modelos disponible.
- Modelo aprobado cargable.
- Red privada operativa.

## Respaldo

Política inicial propuesta:

- Incremental diario.
- Completo semanal.
- Cifrado y checksum.
- Copia fuera de Tezkatli.
- Restauración de prueba mensual.

La frecuencia final se confirma después de medir tamaño y tiempo.

## Actualización

1. Exportar respaldo.
2. Verificar checksum.
3. Ejecutar migración en copia.
4. Ejecutar pruebas rápidas.
5. Desplegar backend antes o después del cliente según matriz de compatibilidad.
6. Observar errores y cola.
7. Conservar rollback compatible.

## Incidentes

### Tezkatli caído

- Android continúa offline.
- No borrar outbox.
- Mostrar trabajos pendientes.
- Recuperar servicio y observar drenaje idempotente.

### Base Android dañada

- No sobrescribir respaldo válido.
- Exportar evidencia diagnóstica saneada.
- Restaurar en ubicación temporal.
- Validar conteos e integridad.

### Modelo defectuoso

- Marcar versión como retirada.
- Cancelar trabajos no iniciados.
- Revertir al modelo aprobado anterior.
- Reprocesar solo por solicitud explícita; no sobrescribir confirmados.

### Token comprometido

- Revocar token.
- Generar credencial nueva.
- Revisar logs saneados y dispositivos.
- No publicar el valor afectado.
