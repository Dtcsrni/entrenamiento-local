# Acta de constitución

## Identificación

- **Nombre del producto:** Gymratic
- **Usuario:** una sola persona
- **Plataforma mínima objetivo:** Realme GT 6
- **Wearable objetivo:** Amazfit Active original
- **Nodo de cómputo:** Tezkatli
- **Estado:** definición y viabilidad

## Problema

Las aplicaciones existentes fragmentan entrenamiento, nutrición, suplementos y wearables; además, sus inferencias suelen depender de servicios externos y no distinguen adecuadamente mediciones, estimaciones y correcciones. Se necesita una solución privada que mantenga el registro rápido durante el gimnasio y permita análisis local reproducible.

## Objetivos

1. Registrar sesiones de fuerza y cardio sin depender de conectividad.
2. Mantener historial preciso por ejercicio, máquina, serie y repetición.
3. Registrar alimentación y suplementos mediante varios métodos de entrada.
4. Reducir la fricción con IA local, manteniendo revisión humana.
5. Generar recomendaciones explicables basadas en reglas, equipo e historial.
6. Integrar Amazfit Active sin convertirlo en fuente definitiva de datos.
7. Proteger y respaldar toda la información personal.

## Alcance inicial

- Cardio inicial, rutina y cardio final.
- Rutinas manuales, editables y sugeridas.
- Catálogo versionado de máquinas del gimnasio, sujeto a verificación física.
- Series, repeticiones, cargas, RIR/RPE, descanso y notas.
- Alimentos por texto, voz, búsqueda, código de barras, OCR y fotografía.
- Componentes y porciones editables con procedencia e incertidumbre.
- Suplementos, dosis, horarios, adherencia e inventario.
- Android local-first, Health Connect opcional y Tezkatli privado.
- Aplicación auxiliar Zepp sujeta a prueba de concepto.

## Fuera del alcance inicial

- Multiusuario, red social o servicio comercial.
- Diagnóstico, tratamiento o prescripción médica.
- Recomendaciones clínicas o automatización de dosis.
- Soporte iOS.
- Nube pública para IA o almacenamiento personal.
- Confirmación automática de repeticiones o alimentos sin revisión.

## Restricciones

- Toda IA debe ejecutarse localmente en el teléfono o Tezkatli.
- El sistema debe seguir siendo útil si Tezkatli no está disponible.
- El Realme GT 6 es el dispositivo Android mínimo de validación.
- La compatibilidad efectiva del Amazfit Active es un dato desconocido hasta la PoC.
- La masa de alimentos inferida desde imágenes es una estimación, no una medición.

## Indicadores de éxito

- Una sesión completa puede registrarse offline sin pérdida de series.
- Una serie normal se completa con máximo dos acciones deliberadas.
- Toda inferencia alimentaria es editable y conserva procedencia.
- Un respaldo puede restaurarse en un entorno limpio.
- La aplicación identifica y comunica datos incompletos o inciertos.
- Los modelos solo se promueven después de superar una línea base documentada.

## Enfoque de ciclo de vida

Iterativo, incremental y dirigido por riesgos. La secuencia detallada está en [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md).
