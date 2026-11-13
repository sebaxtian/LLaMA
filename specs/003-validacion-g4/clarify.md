# Clarificación - SPEC-003

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados).

## Alcance de esta clarificación

- **Spec clarificada:** `spec.md` v0.1.0, `status: draft`, con G1 aprobada por el propietario el 2026-11-13.
- **Versión resultante:** `spec.md` v0.2.0, `status: clarified`.
- **Hallazgos:** AMB-001 a AMB-004.
- **Casos borde nuevos:** ninguno. CB-004 queda confirmado en AMB-001.
- **Requisitos alterados:** ninguno. Los RF, RNF, CB y CA conservan su texto.

## Hallazgos de ambigüedad

### AMB-001 - Alcance de CB-004

- **Pregunta:** ¿debe una spec en estado `validated` o `released` sin reporte de validación producir un error cuando se valida sin indicar compuerta?
- **Respuesta:** sí. CB-004 queda confirmado. El propietario lo aprobó junto con G1.
- **Fecha (UTC):** 2026-11-13.
- **Responsable:** Agent Sebaxtian.
- **Efecto:** CB-004 y el primer escenario de CA-001 se mantienen. Ninguna palabra de `spec.md` cambia.

### AMB-002 - Mecanismo de pruebas en RNF-003

- **Pregunta:** RNF-003 exige pruebas con el mecanismo de la biblioteca estándar, pero no nombra el mecanismo concreto. ¿Qué mecanismo se usa?
- **Respuesta:** `unittest` de la biblioteca estándar. El nombre concreto no va en `spec.md` (PROTOCOLO §4 prohíbe frameworks en la spec). Se registra como decisión técnica DEC-005 en `plan.md`.
- **Fecha (UTC):** 2026-11-13.
- **Responsable:** Agent Sebaxtian.
- **Efecto:** RNF-003 no cambia. El comando de pruebas se fija en `plan.md`.

### AMB-003 - Severidad de la cobertura RF/CB → CA

- **Pregunta:** RF-004 emite una advertencia cuando un RF o CB no aparece en ninguna línea «Cubre:». ¿Debe convertirse en error?
- **Respuesta:** no. La advertencia se mantiene. SPEC-001 no declara líneas «Cubre:», y convertir el aviso en error la invalidaría. Ese cambio queda fuera de alcance (`spec.md`, «Fuera de alcance»).
- **Fecha (UTC):** 2026-11-13.
- **Responsable:** Agent Sebaxtian.
- **Efecto:** RF-004 no cambia. La decisión técnica se registra como DEC-004 en `plan.md`.

### AMB-004 - Semántica del dictamen

- **Pregunta:** ¿cómo se determina el dictamen de un reporte que contiene «NO CONVERGIDO» en prosa?
- **Respuesta:** se evalúa solo la casilla marcada `[x] CONVERGIDO` o `[x] NO CONVERGIDO` en la línea de dictamen. La mención en prosa se ignora. Así «NO CONVERGIDO» en texto libre no se confunde con convergencia.
- **Fecha (UTC):** 2026-11-13.
- **Responsable:** Agent Sebaxtian.
- **Efecto:** la regla de lectura ya consta en el Contexto de `spec.md`. La decisión técnica se registra como DEC-001 en `plan.md`.

## Parches aplicados a spec.md

- [x] P-001 - Frontmatter: `status` pasa de `draft` a `clarified`; `version` pasa de `0.1.0` a `0.2.0`. Origen: AMB-001 y la aprobación de G1.
- [x] P-002 - Sección Aprobaciones: se registra G1 como `- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)`. Origen: aprobación del propietario.
- [x] P-003 - Historial de cambios: fila 0.2.0 «Aprobación G1 y clarificación». Origen: P-001 y P-002.
- [x] P-004 - AMB-001: CB-004 confirmado. Sin cambio de texto.
- [x] P-005 - AMB-002, AMB-003 y AMB-004: sin cambio de texto. Las decisiones quedan en `plan.md` (DEC-005, DEC-004 y DEC-001).
