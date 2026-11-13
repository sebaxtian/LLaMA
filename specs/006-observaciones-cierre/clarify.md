# Clarificación - SPEC-006

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** La fila de `sdd` en la tabla de agentes y permisos del protocolo operativo (§10) no usa la expresión literal «orquestador de solo lectura sobre artefactos y código» que exige RF-005 de SPEC-005.
- **Pregunta:** ¿Qué texto exacto debe tener la fila de `sdd` en §10?
- **Respuesta:** Rol: «Orquestador de solo lectura sobre artefactos y código; registro de cambios Git de artefactos de control». Permisos: «Puede lanzar subagentes y ejecutar `git add` y `git commit` de artefactos de control».
- **Decisión:** Se aplica en RF-001 y CA-001 de `spec.md` y en DEC-001 de `plan.md`. El literal exacto se usa en el rol y el límite del bookkeeping Git se expresa en los permisos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** La memoria operativa no enumera el agente `documenter` ni explica cómo consultar los agentes del proyecto (RF-002).
- **Pregunta:** ¿Qué debe contener la memoria operativa sobre los agentes?
- **Respuesta:** Enumerar `sdd`, `planner`, `coder`, `reviewer` y `documenter`, y aclarar que `explore` es un subagente integrado de OpenCode. Documentar que `opencode debug agents` debe ejecutarse con el directorio de trabajo en la raíz del repositorio. El propietario indicó además documentar el parámetro `location[directory]` de la API.
- **Verificación durante la clarificación:** `opencode debug agents` ejecutado desde la raíz del repositorio lista `sdd`, `planner`, `coder`, `reviewer` y `documenter`, junto con `explore` y los agentes integrados. Ejecutado desde otro directorio no lista ninguno de los agentes del proyecto (CB-002). El parámetro `location[directory]` no pudo verificarse: las rutas de la API probadas (`GET /agent`, `GET /agents`, `GET /experimental/agent`) no devolvieron la lista de agentes. Por ello la memoria operativa no documenta ese parámetro hasta comprobarlo.
- **Decisión:** Se aplica en RF-002 y CA-002 de `spec.md` y en DEC-002 de `plan.md`. El comando verificado desde la raíz es la forma documentada. El parámetro `location[directory]` queda como punto pendiente de confirmación por el propietario, sin afectar al requisito RF-002.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** La confirmación explícita de AMB-001 de SPEC-005 (regla de celda superada) no consta en la clarificación de SPEC-005, que dejó ese punto como «a confirmar por el propietario».
- **Pregunta:** ¿Cómo debe registrarse la confirmación del propietario?
- **Respuesta:** El propietario confirmó explícitamente la regla: solo cuenta como superada una celda PASADO con paréntesis de observación opcional. NO PASADO, PENDIENTE, PARCIAL y las celdas compuestas con estado negativo son error.
- **Decisión:** Se añade una nota con fecha 2026-11-13 y responsable Agent Sebaxtian al final de la clarificación de SPEC-005, sin alterar sus decisiones (DEC-003 de `plan.md`). Se aplica en RF-003 y CA-003 de `spec.md`.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

No se añaden casos borde nuevos. CB-001 y CB-002 de `spec.md` no cambian.

## Parches aplicados a `spec.md`

- [x] Restricción de ejecutores (Contexto y Actores): se corrige la afirmación de que ningún agente puede editar la memoria operativa y el registro de cambios. El agente `coder` tiene permiso de edición fuera de `specs/**` y `docs/**`, por lo que sí puede ejecutar T-002 y T-004. Sin cambio de requisitos (verificación de permisos de la etapa Tasks).
- [x] RF-001, RF-002 y RF-003 y sus criterios CA-001 a CA-003 ya recogen los textos decididos en AMB-001 a AMB-003. Sin cambio adicional.

## Decisiones de negocio

- No se modifican agentes, comandos ni permisos de `.opencode/`. Si T-002 o T-004 requirieran otro permiso, se aplica CB-001 y se reporta.
- El parámetro `location[directory]` de la API no se documenta hasta verificarlo. El propietario debe confirmar si mantiene esa indicación.
- La clasificación de `explore` como integrado se mantiene: no está en `.opencode/agents/`.
