# Análisis de aplicaciones de referencia

## Síntesis

| Referencia | Fortaleza que se adopta | Decisión |
|---|---|---|
| Hevy/Strong | Registro de fuerza de baja fricción | Valores previos, temporizador, RPE/RIR, undo y proyecciones |
| Fitbod | Filtrado por equipo y adaptación | Motor determinista de restricciones/puntuación y explicación |
| MacroFactor | Tendencias y ajuste conservador | Peso tendencial, calidad de evidencia y revisión semanal |
| Cronometer | Procedencia nutricional | Calidad por fuente y múltiples métodos de captura |
| MyFitnessPal | Reutilización rápida | Recientes, comidas, recetas, copia y Quick Add |
| Foodvisor/SnapCalorie | Fotografía editable | Borrador por componentes, nunca confirmación automática |
| wger | Offline y sincronización | SQLite/Room local y cola, sin copiar su infraestructura multiusuario |
| Open Food Facts | Productos/taxonomías | Adaptador con validación y procedencia |
| Health Connect | Interoperabilidad | Adaptador opcional con origen y deduplicación propia |
| Zepp OS | Puente reloj–teléfono–servidor | Device App + Side Service condicionado por hardware |

## Elementos rechazados

- Red social y rankings.
- Gamificación invasiva.
- Recuperación fisiológica mostrada como porcentaje cierto.
- Rutinas creadas directamente por un LLM.
- Calorías visuales presentadas como mediciones.
- Infraestructura multiusuario sin necesidad.
- Conteo automático confirmado sin revisión.

## Ventaja objetivo

La diferenciación no consiste en más funciones, sino en integrar los dominios bajo trazabilidad explícita: origen, método de medición, versión de algoritmo, incertidumbre y confirmación.
