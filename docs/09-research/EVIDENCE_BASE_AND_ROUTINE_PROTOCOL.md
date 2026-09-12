# Base de evidencia y protocolo para rutinas

**Identificador:** RES-EVIDENCE-BASE
**Versión:** 1.0
**Fecha de adopción:** 2026-09-12
**Estado:** Normativo para el diseño, revisión y seguimiento de rutinas

## 1. Propósito

Toda rutina y toda característica prescrita por el proyecto deberá basarse en fuentes científicas y médicas identificables, actuales y adecuadas para la población objetivo. La aplicación no presentará como hecho clínico una inferencia de una fuente comercial, una imagen, una preferencia personal o una única investigación aislada.

Esta política cubre, como mínimo:

- selección y orden de ejercicios;
- prioridad de máquinas, poleas o peso libre;
- volumen, frecuencia, series, repeticiones, carga y descansos;
- esfuerzo, RIR/RPE, fallo y progresión;
- rango de movimiento, técnica y calentamiento;
- cardio, duración estimada y recuperación;
- advertencias, cribado y límites médicos.

No sustituye diagnóstico, tratamiento, rehabilitación ni autorización médica. El marco general de entrenamiento se apoya principalmente en adultos sanos; las enfermedades, lesiones, embarazo, síntomas, medicación o restricciones clínicas requieren evidencia específica y, cuando corresponda, revisión de un profesional sanitario.

## 1.1 Requisitos verificables

- **RES-EVD-001 · P0:** cada rutina deberá conservar un mapa de afirmaciones, fuentes, población, desenlace y limitaciones. **Criterio:** no puede alcanzar `EVIDENCE_REVIEWED` si falta una fuente para una afirmación cuantitativa.
- **RES-EVD-002 · P0:** cada prescripción numérica deberá distinguir evidencia directa, inferencia y decisión personal. **Criterio:** la ficha muestra la etiqueta y la justificación de series, repeticiones, carga, descanso, esfuerzo y frecuencia.
- **RES-EVD-003 · P0:** toda recomendación con implicación médica deberá usar una guía clínica o sanitaria aplicable y definir derivación. **Criterio:** condiciones no cubiertas permanecen fuera del alcance de la automatización.
- **RES-EVD-004 · P0:** las fuentes y decisiones deberán ser versionadas y revisadas periódicamente. **Criterio:** cada registro incluye PMID/DOI o URL primaria, fecha de consulta, versión y limitaciones.
- **RES-EVD-005 · P1:** la prioridad de máquinas deberá tratarse como restricción/preferencia y no como superioridad fisiológica universal. **Criterio:** cada selección separa evidencia de adaptación de evidencia de equipo.

## 2. Jerarquía de evidencia

| Nivel | Fuente aceptable | Uso permitido |
|---|---|---|
| A | Guías de organismos sanitarios, position stands de sociedades profesionales, revisiones sistemáticas y metaanálisis de ensayos humanos | Base principal para recomendaciones y rangos cuantitativos |
| B | Ensayos controlados, estudios longitudinales y estudios observacionales relevantes | Resolver preguntas concretas cuando no exista evidencia A suficiente; declarar limitaciones |
| C | Estudios biomecánicos, fisiológicos, de técnica o de especificidad del equipo | Describir ejecución, ajustes, trayectoria y transferencia; no demostrar por sí solos superioridad clínica o hipertrofia |
| D | Manuales del fabricante, fotografías verificadas y documentación del gimnasio | Identificar una máquina, sus ajustes y su disponibilidad; no sustentar efectos fisiológicos |
| E | Opinión de experto, contenido comercial o divulgación | Solo generar hipótesis o alternativas pendientes; nunca justificar por sí solo una prescripción definitiva |

La calidad y aplicabilidad se registrarán separadamente. Una fuente de nivel A sobre adultos sanos no se extrapola automáticamente a una persona con una condición médica.

## 3. Biblioteca mínima vigente

Esta biblioteca constituye el conjunto mínimo para construir las rutinas actuales. No se considera cerrada: se ampliará por objetivo, población o condición clínica.

### Marco general de actividad física y seguridad

1. [WHO Guidelines on physical activity and sedentary behaviour](https://www.who.int/publications/i/item/9789240014886) (WHO, 2020). Base de frecuencia, intensidad, duración, sedentarismo y subpoblaciones.
2. [PAR-Q+ / ePARmed-X+](https://eparmedx.com/) (PAR-Q+ Collaboration, versión vigente). Cribado inicial y derivación; no es diagnóstico ni sustituye valoración clínica.

### Prescripción de fuerza, hipertrofia y rendimiento

3. [ACSM Position Stand: Resistance Training Prescription for Muscle Function, Hypertrophy, and Physical Performance in Healthy Adults](https://pubmed.ncbi.nlm.nih.gov/41843416/) (Currier et al., 2026). Actualiza el position stand de 2009 y sintetiza 137 revisiones con más de 30,000 participantes.
4. [Resistance training prescription for muscle strength and hypertrophy in healthy adults](https://pubmed.ncbi.nlm.nih.gov/37414459/) (Nunes et al., 2023). Revisión sistemática y network meta-analysis de cargas, series y frecuencia.
5. [The Resistance Training Dose Response](https://pubmed.ncbi.nlm.nih.gov/41343037/) (Pelland et al., 2026). Metarregresiones de volumen y frecuencia, distinguiendo series directas e indirectas y posibles rendimientos decrecientes.
6. [Dose-response relationship between weekly resistance training volume and increases in muscle mass](https://pubmed.ncbi.nlm.nih.gov/27433992/) (Schoenfeld et al., 2017). Relación entre series semanales y masa muscular; se usará junto con evidencia más reciente, no como umbral universal.
7. [Influence of resistance training load on hypertrophy and maximal strength](https://pubmed.ncbi.nlm.nih.gov/33874848/) (Refalo et al., 2021). Diferencia entre efectos sobre hipertrofia y fuerza según la carga.
8. [Effects of resistance training performed to failure or non-failure](https://pubmed.ncbi.nlm.nih.gov/33497853/) (Grgic et al., 2022) y [proximity-to-failure](https://pubmed.ncbi.nlm.nih.gov/36334240/) (Refalo et al., 2023). El fallo no se tratará como requisito universal; el esfuerzo se prescribirá según objetivo, ejercicio, fatiga y seguridad.

### Selección de máquinas y variables de sesión

9. [Machines and free weight exercises: systematic review and meta-analysis](https://pubmed.ncbi.nlm.nih.gov/34609100/) (Heidel et al., 2022). No demuestra superioridad general de máquinas para hipertrofia; permite priorizarlas por estabilidad, preferencias, disponibilidad y especificidad del objetivo.
10. [Give it a rest: inter-set rest interval and muscle hypertrophy](https://pubmed.ncbi.nlm.nih.gov/39205815/) (Singer et al., 2024). Base para ajustar descansos sin imponer falsa precisión; los efectos dependen de volumen, ejercicio y población.
11. [The effect of muscle warm-up on force-time parameters](https://pubmed.ncbi.nlm.nih.gov/39864808/) (Wilson et al., 2025). Base actual para calentamientos; no se asumirá que una modalidad concreta sea universalmente superior.

## 4. Requisitos para aprobar una rutina

Una rutina no podrá marcarse como `EVIDENCE_REVIEWED` hasta que su ficha incluya:

1. objetivo principal y secundarios;
2. población, nivel de entrenamiento y supuestos de salud;
3. selección de cada ejercicio y función que cubre;
4. series efectivas, repeticiones, carga o rango de intensidad, descansos, esfuerzo y progresión;
5. calentamiento y cardio, con fundamento separado del trabajo de fuerza;
6. estimación de duración con fórmula y supuestos explícitos;
7. alternativas por disponibilidad, dolor, limitación funcional o preferencia;
8. advertencias y criterios de pausa o derivación;
9. mapa `claim → source → population → outcome → limitation`;
10. fecha de revisión y versión de la evidencia.

Cada afirmación cuantitativa deberá tener al menos una fuente de nivel A o B. Si solo existe evidencia indirecta, se etiquetará como `INFERRED` y no como hecho demostrado.

## 5. Regla para prioridad de máquinas

El proyecto puede priorizar máquinas porque es una restricción y preferencia del usuario, favorece estabilidad, disponibilidad y progresión reproducible, y puede mejorar la especificidad de la prueba de fuerza. Esa prioridad no deberá expresarse como una superioridad general de las máquinas para hipertrofia: la revisión disponible no encontró diferencias globales claras de hipertrofia entre máquinas y peso libre, y la fuerza depende en parte de la especificidad del modo de entrenamiento.

Por tanto, cada ejercicio de máquina deberá conservar:

- nombre y variante exactos;
- máquina o familia de equipo;
- ajustes relevantes;
- músculo o función objetivo;
- evidencia fisiológica separada de la evidencia de identificación del equipo;
- alternativa funcional si la estación no está disponible.

## 6. Límites médicos y control de riesgo

- No se diagnosticará, prescribirá medicación ni modificará dosis de suplementos o fármacos.
- Dolor agudo, síntomas cardiovasculares, neurológicos, respiratorios, pérdida de función o empeoramiento persistente detienen la progresión automática y requieren evaluación apropiada.
- Una condición clínica solo se incorporará con una guía específica de una organización sanitaria o sociedad profesional, evidencia clínica relevante y límites de derivación.
- La rutina general para adultos sanos no se presentará como rehabilitación.
- Las recomendaciones de seguridad deberán indicar población, contexto, fecha y nivel de certeza.

## 7. Actualización y trazabilidad

- Revisión bibliográfica mínima: cada 12 meses y antes de cambiar una recomendación P0.
- Revisión extraordinaria: nueva guía, position stand, alerta de seguridad o metaanálisis que cambie materialmente una conclusión.
- Toda fuente se registrará con autores, año, título, DOI o PMID, población, intervención, comparador, desenlaces, limitaciones y fecha de consulta.
- Las fuentes comerciales o del fabricante se conservarán solo para propiedades del equipo y no reemplazarán la literatura clínica.
- El cambio de una rutina deberá identificar qué afirmaciones cambian, qué fuentes las sustentan y qué validación humana permanece pendiente.

## 8. Estado de adopción

Esta política queda adoptada como criterio de aceptación para las rutinas del proyecto. Las rutinas existentes deberán migrarse progresivamente a este protocolo; hasta completar su mapa de evidencia, su estado será `LEGACY_UNMAPPED` y no `EVIDENCE_REVIEWED`.
