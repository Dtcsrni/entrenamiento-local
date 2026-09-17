# Desarrollo asistido por IA generativa

## Propósito

Codex se utiliza como agente técnico para inspeccionar, diseñar, implementar y
validar cambios locales. No sustituye la responsabilidad humana sobre el
alcance, los requisitos, la seguridad, los datos confirmados ni la aceptación
del producto.

El procedimiento es independiente del modelo concreto. En cada trabajo se
registrará el modelo y configuración usados cuando sean relevantes para
reproducir el resultado; no se debe asumir que una versión del modelo garantiza
compatibilidad, precisión o ausencia de defectos.

## Ciclo obligatorio por incremento

1. **Definir:** objetivo, contexto, restricciones, riesgos, criterio de
   aceptación y archivos dentro de alcance.
2. **Inspeccionar:** leer instrucciones, contratos, usos, dependencias y
   pruebas; identificar cambios concurrentes y datos sensibles.
3. **Diseñar:** elegir el cambio mínimo, conservar interfaces y registrar una
   ADR cuando la decisión sea arquitectónicamente significativa.
4. **Implementar:** cambios pequeños y reversibles, sin secretos ni datos
   personales; la IA no escribe directamente datos confirmados del dominio.
5. **Verificar:** ejecutar pruebas específicas, compilación, lint y validadores
   aplicables. Un comando que termina por timeout o que no descubre pruebas no
   cuenta como validación.
6. **Revisar:** inspeccionar el diff, trazabilidad, seguridad, límites y efectos
   laterales; separar resultado medido de propuesta o inferencia.
7. **Aceptar:** la persona responsable decide si el cambio se incorpora,
   publica o se promociona a una ruta de producción.

## Estados de evidencia

- `PROPOSED`: diseño o salida generativa aún no ejecutada.
- `IMPLEMENTED`: código o documentación materializada.
- `MEASURED`: resultado obtenido mediante un procedimiento reproducible.
- `AGENT_REVIEWED`: revisión automática/técnica ejecutada por Codex.
- `HUMAN_CONFIRMED`: aceptación explícita de una persona con autoridad.

Estos estados no son intercambiables: pasar pruebas no equivale a validación
humana, y una propuesta de IA no equivale a un dato confirmado.

## Límites de autonomía

Se permiten dentro del alcance: lectura del repositorio, edición local,
pruebas no destructivas y generación de artefactos sintéticos. Requieren
confirmación explícita: publicación externa, cambios destructivos, compras,
credenciales, secretos, datos personales y ampliaciones materiales de alcance.

## Criterio de cierre

Un incremento solo se cierra cuando su criterio de aceptación está satisfecho,
las pruebas realmente se ejecutaron, el diff no contiene cambios ajenos, la
documentación y trazabilidad están actualizadas y los riesgos pendientes están
declarados.

Como orientación específica del uso de modelos OpenAI, consultar la
[documentación oficial de guía de modelos y prácticas de trabajo](https://developers.openai.com/api/docs/guides/latest-model).
