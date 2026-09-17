# Matriz inicial de trazabilidad

La matriz crecerá con la implementación. `Planned` significa que no existe todavía evidencia ejecutada.

| Requisito | Riesgo | Diseño/ADR | Prueba prevista | Estado |
|---|---|---|---|---|
| FUN-TRN-001 | RISK-004 | ADR-003 | TST-TRN-001 | Planned |
| FUN-TRN-003 | RISK-004 | ADR-003 | TST-TRN-002 | Planned |
| FUN-TRN-005 | RISK-004 | ADR-003 | TST-TRN-003 | Planned |
| FUN-GYM-001 | RISK-007, RISK-008 | ADR-012 | TST-GYM-001 | Planned |
| FUN-NUT-001 | RISK-006 | ADR-007 | TST-NUT-001 | Planned |
| FUN-NUT-002 | RISK-002, RISK-009 | ADR-006 | TST-NUT-002 | Planned |
| FUN-NUT-003 | RISK-002 | ADR-006 | TST-NUT-003 | Planned |
| FUN-AI-001 | RISK-003, RISK-005 | ADR-005 | TST-AI-001 | Planned |
| FUN-AI-002 | RISK-012 | ADR-006 | TST-AI-002 | Planned |
| FUN-AI-003 | RISK-012 | ADR-006 | TST-CON-001 | Implemented |
| FUN-WEA-001 | RISK-001 | ADR-012 | TST-WEA-001 | Planned |
| FUN-SYN-001 | RISK-003 | ADR-003 | TST-SYN-001 | Planned |
| FUN-SYN-002 | RISK-004 | ADR-004 | TST-SYN-002 | Planned |
| NFR-COM-001 | RISK-004 | ADR-001 | TST-CON-001 | Implemented |
| FUN-EXP-001 | RISK-014 | ADR-011 | TST-REC-001 | Planned |
| NFR-SEC-001 | RISK-003, RISK-010 | ADR-008 | TST-SEC-001 | Planned |
| NFR-REL-001 | RISK-004 | ADR-003, ADR-004 | TST-REL-001 | Planned |
| NFR-AI-001 | RISK-009 | ADR-006 | TST-AI-003 | Planned |

## Serie TDD/SDD

| Diseño | Requisitos/riesgos principales | Pruebas | Estado inicial |
|---|---|---|---|
| SDD-001 · Rutina canónica y versionado | Contenido de `DIA_1/2/3_CONTENIDO_Y_MAQUETACION`, RISK-011 | TDD-002 / `TST-CAN-001..002` | In progress |
| SDD-002 · Plantilla y máquina de estados UI | FUN-TRN-001, FUN-TRN-006, NFR-USA-001 | TDD-003 / `TST-CAN-003`, `TST-UI-*` | Partial |
| SDD-003 · Medios y procedencia | NFR-SEC-002, NFR-PRI-002, límites de evidencia | TDD-004 / `TST-MED-*` | In progress |
| SDD-004 · Builders y PWA | NFR-COM-001, RISK-011 | TDD-001/TDD-005 / `TST-BLD-001` | Partial |
| SDD-005 · Entrenamiento local-first | FUN-TRN-001..009, RISK-004 | TDD-006 / `TST-TRN-*`, `TST-REL-001` | Planned |
| SDD-006 · Outbox y recuperación | FUN-SYN-001..004, FUN-EXP-001..002, RISK-004/RISK-014 | TDD-007 / `TST-SYN-*`, `TST-REC-001` | Planned |
| SDD-007 · Nutrición e IA | FUN-NUT-001..009, FUN-AI-001..006, RISK-002/RISK-009/RISK-012 | TDD-008 / `TST-NUT-*`, `TST-AI-*` | Planned |
| SDD-008 · Integraciones externas | FUN-WEA-001..004, FUN-HC-001..002, RISK-001/RISK-003 | TDD-009 / `TST-WEA-*` | Planned |
| SDD-009 · Seguridad, rendimiento y operación | NFR-REL, NFR-PER, NFR-SEC, RISK-003/RISK-005/RISK-010 | TDD-010 / `TST-SEC-*` | Planned |

## Evidencia científica y límites médicos

| Requisito | Fuente/protocolo | Criterio de aceptación | Estado |
|---|---|---|---|
| RES-EVD-001 | EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md §1.1, §4 | Cada afirmación cuantitativa de una rutina tiene fuente, población, desenlace y limitaciones | Planned |
| RES-EVD-002 | EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md §2, §4 | La ficha separa hecho, inferencia y decisión personal para todas las variables de prescripción | Planned |
| RES-EVD-003 | EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md §6 | Las condiciones médicas usan evidencia clínica aplicable o quedan fuera de la automatización | Planned |
| RES-EVD-004 | EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md §7 | Cada fuente tiene PMID/DOI o URL primaria, fecha, versión y limitaciones | Implemented |
| RES-EVD-005 | EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md §5 | La prioridad de máquinas aparece como restricción/preferencia y no como superioridad universal | Planned |
