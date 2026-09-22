# ADR-014 — Progresión y avisos locales de la PWA

**Estado:** Superseded por ADR-015
**Fecha:** 2026-09-22

## Contexto

La PWA permite marcar series y conserva sesiones, pero no registra repeticiones ni carga por serie. El usuario quiere revisar progreso, conservar el nombre y el historial, y recibir avisos según días habituales sin fijar una asistencia rígida ni cambiar el plan actual.

## Decisión

1. La portada guarda las preferencias de aviso junto al perfil local. La versión actual del perfil es `schemaVersion=3`.
2. Las copias `gymratik-backup` usan `schemaVersion=3`; el importador admite únicamente ese esquema.
3. Las repeticiones y cargas opcionales se agregan como datos aditivos a cada sesión, por ejercicio y serie. No se crea un servicio remoto ni se usa un nuevo almacén que requiera reconstrucción de historiales.
4. La pauta de doble progresión usa el rango de repeticiones ya publicado para el ejercicio: si todas las series de la última sesión alcanzan el límite superior con la misma carga registrada, sugiere considerar el incremento mínimo disponible; en otro caso, mantener la carga e intentar añadir repeticiones. Es una ayuda condicional, no una orden ni una decisión automatizada. Requiere que se mantengan técnica y esfuerzo apropiados; no representa una evaluación de RIR porque ese dato no se captura.
5. La interfaz calcula los días más frecuentes entre sesiones de las últimas ocho semanas como sugerencia descriptiva. El usuario puede seleccionar cualquier combinación de días, conservar flexibilidad y descartar el aviso por fecha.
6. El aviso se evalúa cuando la portada se abre o vuelve a primer plano. Se muestra dentro de la PWA, se omite si ya se inició una sesión ese día y nunca se afirma que llegue con la aplicación cerrada. No se solicita permiso del sistema operativo.
7. La rutina no se adapta al objetivo del perfil ni cambia por calendario. La selección de ejercicios y volumen se mantiene mientras sea tolerable y haya avance; los bloqueos persistentes, problemas de recuperación/adherencia, dolor y cambios contextuales justifican revisión humana.
8. Nombre, preferencias, sesiones y rendimiento permanecen en IndexedDB/localStorage según el almacén existente y en los respaldos que el usuario exporta. No se envían a servicios remotos. La protección depende del dispositivo, perfil del navegador y acceso al archivo de respaldo.

## Consecuencias

- Esta decisión fue supersedida por ADR-015 para fijar los esquemas actuales y su compatibilidad.
- La PWA puede mostrar avisos solo durante uso activo; no puede garantizar entrega en segundo plano.
- Los valores de carga entre máquinas no siempre son comparables; los registros se asocian al ejercicio/rutina y deben interpretarse en el contexto del mismo equipo y su configuración.
- Un usuario puede completar series sin capturar carga o repeticiones; en ese caso no se emite una recomendación cuantitativa para esas series.
- Los datos locales no se cifran y no resisten el compromiso del dispositivo o código ejecutado en el mismo origen. El respaldo puede exponer datos si se comparte.

## Verificación

- Perfil y respaldo v3, rechazo de esquemas anteriores e importación/exportación de extremo a extremo: `tests/test_progress_store_runtime.py`.
- Rendimiento de series completadas y sanitización de reps/carga: `tests/test_progress_store_runtime.py`.
- Reglas de historial, sugerencia de días y aviso local: `tests/test_homepage.py`.
- Builders canónicos, `python scripts/validate_repository.py` y `python -m unittest discover -s tests -p "test_*.py"`.

## Fuentes de decisión sobre estabilidad del plan

- [ACSM Position Stand 2026](https://pubmed.ncbi.nlm.nih.gov/41843416/): overview de 137 revisiones y más de 30,000 participantes; el rango de 6–52 semanas describe duración de estudios elegibles, no una instrucción de cambiar la rutina tras cierto plazo. La periodización no afectó consistentemente resultados incluidos.
- [Moesgaard et al. 2022](https://pubmed.ncbi.nlm.nih.gov/35044672/): 35 estudios; periodizar favoreció modestamente el 1RM cuando se equiparó volumen (ES 0.31), sin diferencia detectada para hipertrofia.
- [Kassiano et al. 2022](https://pubmed.ncbi.nlm.nih.gov/35438660/): revisión de 8 estudios (241 participantes, todos varones jóvenes); sugiere distinguir variación planificada de cambios excesivos o aleatorios. La población y el tamaño limitan generalización.

Interpretación de producto: “varios meses” puede servir como primera ventana de revisión, pero no es una prescripción científica fija ni un mínimo obligatorio. La progresión y tolerancia guían la continuidad; no se reemplaza la rutina automáticamente.
