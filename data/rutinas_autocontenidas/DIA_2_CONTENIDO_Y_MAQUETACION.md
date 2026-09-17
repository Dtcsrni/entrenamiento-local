# Día 2 · Pierna + Glúteo · contenido y maquetación

## Estado y objetivo

La versión canónica es `canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html`. Su objetivo es presentar una sesión de tren inferior para un adulto sano con prioridad práctica en máquinas, 20 series efectivas, instrucciones visuales y progresión reproducible.

La prioridad de máquinas es una restricción y preferencia de diseño: favorece estabilidad, disponibilidad y registro de carga. El hip thrust se presenta en máquina, de acuerdo con la referencia de equipo y la secuencia de fases de la fuente local. No se presenta la selección como superioridad fisiológica universal frente al peso libre.

La maquetación hereda directamente la plantilla canónica vigente del Día 1: cabecera de sesión, guía rápida, calentamiento visual, seguimiento del calentamiento, resumen de sesión, progreso de las 20 series, tarjetas de ejercicio, reglas de ejecución y reinicio de sesión. El builder toma el HTML del Día 1 como `TEMPLATE` para evitar una segunda plantilla divergente.

## Prescripción aprobada

| # | Ejercicio | Series | Repeticiones | Descanso | Función principal |
|---:|---|---:|---:|---:|---|
| 1 | Hack squat | 3 | 6–8 | 3 min | Sentadilla guiada; cuádriceps y glúteo |
| 2 | Hip thrust en máquina | 3 | 6–10 | 2.5–3 min | Extensión de cadera; glúteo mayor |
| 3 | Prensa de piernas | 3 | 8–12 | 2–3 min | Extensión de rodilla y cadera |
| 4 | Curl femoral en máquina | 4 | 8–12 | 2 min | Flexión de rodilla; isquiosurales |
| 5 | Extensión de piernas | 3 | 10–15 | 90–120 s | Extensión de rodilla; cuádriceps |
| 6 | Pantorrillas de pie | 4 | 8–12 | 90–120 s | Flexión plantar; gastrocnemio y sóleo |

La suma es `3 + 3 + 3 + 4 + 3 + 4 = 20` series efectivas. Las series de aproximación no se contabilizan. El cuarto set se asigna al curl femoral para mejorar la cobertura directa de isquiosurales sin añadir otra serie pesada a hack squat o prensa.

## Criterio científico aplicado

- La revisión de posición de **ACSM 2026** sintetiza 137 revisiones y respalda que el entrenamiento de resistencia mejora la hipertrofia; el volumen mayor suele ayudar con rendimientos decrecientes, el rango completo es útil y no hay un efecto consistente del tipo de equipo sobre la hipertrofia.
- La metarregresión de **Pelland et al. 2026** respalda una relación positiva entre volumen y masa muscular, con rendimientos decrecientes; las series indirectas deben contarse con cautela.
- La revisión de **Robinson et al. 2024** indica que la hipertrofia tiende a aumentar al terminar más cerca del fallo, pero no convierte el fallo momentáneo en requisito. Por eso se usa RIR 2–3 al inicio y RIR 1–2 al final o en aislamientos.
- La revisión de **Singer et al. 2024** sugiere una pequeña ventaja de descansos mayores de 60 s y no detecta una ventaja apreciable al superar aproximadamente 90 s de forma general; los compuestos pesados conservan descansos más largos para proteger el rendimiento.
- La revisión de **Nunes et al. 2021** no encontró diferencia consistente de hipertrofia por orden, pero el ejercicio prioritario se coloca primero para proteger el rendimiento agudo.

Fuentes primarias de síntesis: [ACSM 2026](https://pubmed.ncbi.nlm.nih.gov/41843416/), [Pelland et al. 2026](https://pubmed.ncbi.nlm.nih.gov/41343037/), [Robinson et al. 2024](https://pubmed.ncbi.nlm.nih.gov/38970765/), [Singer et al. 2024](https://pubmed.ncbi.nlm.nih.gov/39205815/) y [Nunes et al. 2021](https://pubmed.ncbi.nlm.nih.gov/32077380/).

## Calentamiento y duración

- Cardio suave: `5–8 min`, intensidad conversacional.
- Movilidad dinámica: `3–5 min`, cadera, rodilla y tobillo, sin dolor ni rebotes.
- Aproximación: `2–3 series` progresivas antes del primer ejercicio pesado; no son series efectivas.
- Duración operativa: `65–85 min` como estimación, calculada a partir de 8–13 min de preparación, aproximadamente 49–59 min de trabajo y descansos, y 8–13 min de transiciones/ajustes. Es una estimación, no una medición individual.

## Reglas de progresión y seguridad

Completa el extremo alto del rango en todas las series con técnica estable y RIR objetivo; después aumenta ligeramente la carga y vuelve al extremo bajo. Si el apoyo, la alineación o el control pélvico se deterioran, reduce la carga o aumenta el descanso. Dolor agudo, síntomas neurológicos, respiratorios o cardiovasculares, o pérdida clara de función requieren detener la sesión y buscar valoración apropiada.

## Medios y límites de evidencia

La ficha canónica integra secuencias Inicio → Final con fotografías reales embebidas y GIFs de patrón guiado donde existe un recurso de ejercicio pertinente. La revisión visual confirmó correspondencia suficiente para hack squat, prensa, curl femoral, extensión de piernas y pantorrillas. Para el hip thrust se incorporó el panel `CORRECT FORM` de una demostración oficial de Booty Builder: el recorte muestra repeticiones completas en una máquina, con espalda apoyada, pies firmes, extensión de cadera y regreso controlado. Se excluyó por completo el panel `INCORRECT FORM`. Se retiraron las fotos heredadas de barra porque no representaban el equipo prescrito y se añadieron cuadros estáticos de inicio y final extraídos del mismo panel correcto.

Los cinco GIFs del repositorio son ilustraciones de 180×180 px, semánticamente coincidentes con hack squat, prensa, curl femoral, extensión de piernas y pantorrillas. El sexto recurso es un recorte de 360×180 px y 8.58 s del panel correcto del video oficial; se conserva la relación panorámica para que se vean simultáneamente la persona, la máquina y el recorrido. Sus cuadros de inicio y final también se usan como imágenes estáticas en la secuencia técnica. El calentamiento incorpora seis GIFs adicionales del repositorio, todos de 180×180 px: tres máquinas de cardio (elíptica, bicicleta fija y caminadora) y tres movimientos de movilidad (cadera/rodilla en cuadrupedia, círculos de tobillo y círculos de rodilla). Todos se muestran como apoyo de patrón junto con la secuencia fotográfica y el checklist. La búsqueda de los 1,324 registros del repositorio por `hip thrust`, `glute bridge`, `glute` e `hip`, restringida a `leverage machine`, no encontró coincidencia exacta; el GIF y sus cuadros del video externo se usan sólo en la copia local personal solicitada.

El calentamiento usa GIFs del repositorio con miniaturas estáticas de respaldo; cada medio tiene texto alternativo específico y mantiene soporte para `prefers-reduced-motion`. La procedencia individual de las fotografías embebidas no está trazada en el HTML fuente; permanece pendiente.

## Criterios de aceptación

- El encabezado y dashboard muestran exactamente `20 series efectivas`.
- Las métricas de tarjetas muestran `3, 3, 3, 4, 3, 4` series.
- La cabecera, guía rápida, calentamiento, resumen, tarjetas y cierre siguen la jerarquía del Día 1.
- El seguimiento del calentamiento y el progreso de sesión están presentes y conservan los identificadores funcionales del template (`warmupTracker`, `sessionGamification`, `resetSession`).
- El hip thrust se identifica como ejercicio en máquina; su referencia de equipo y guía estática de fase no mezclan imágenes de barra.
- Los doce recursos animados de ejercicios y calentamiento tienen ruta local y texto alternativo específico; los seis medios del calentamiento y los seis de las tarjetas se insertan sólo donde el patrón coincide.
- Los once GIFs del repositorio se renderizan a su resolución nativa de 180×180 px; el recorte de video real del hip thrust se renderiza a 360×180 px. Todos tienen miniatura estática de respaldo si fallan y el manifiesto documenta su procedencia.
- La ficha conserva alternativas, RIR, progresión, señales de detención y límites de evidencia.
- Se ejecuta `python scripts/validate_repository.py` y se revisa el render en escritorio y móvil.
