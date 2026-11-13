# Clarificación — SPEC-004

## Estado

- [x] Cerrado (todos los AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** La spec no fija el nombre ni la ubicación del archivo que define el subagente `documenter`, ni su modo de operación.
- **Pregunta:** ¿Dónde se define el subagente y con qué modo de operación?
- **Respuesta:** Se define en `.opencode/agents/documenter.md` con modo `subagent`.
- **Decisión:** Corrección de precisión, desarrollada en `plan.md` (DEC-001). Sin cambio de requisitos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** RF-002, RF-003, CB-002 y CB-003 exigen restricciones de edición y de subagentes, pero no fijan las reglas literales.
- **Pregunta:** ¿Qué reglas exactas de edición y de subagentes tiene `documenter`?
- **Respuesta:** Denegar toda edición (`edit *`), permitir `docs/**` y `AGENTS.md`, y denegar el lanzamiento de subagentes (`subagent *`). Sin ningún permiso sobre `specs/`, `src/`, `tools/` ni `.opencode/`.
- **Decisión:** Corrección de precisión, desarrollada en `plan.md` (DEC-001). Sin cambio de requisitos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** RF-006 indica qué debe alinearse, pero no fija el texto de cada documento ni el contenido de la excepción de contabilidad del commit de release.
- **Pregunta:** ¿Qué debe decir exactamente cada documento afectado por O-02?
- **Respuesta:**
  - (a) `docs/sdd/PROTOCOLO_OPERATIVO.md` §6 pasa a decir: «G4: el propietario aprueba la implementación validada (validation_report.md al 100 %)».
  - (b) `AGENTS.md` pasa de «G4 (implementación)» a «G4 (implementación validada)».
  - (c) `docs/Flujo_de_Trabajo_Git.md` documenta que el commit de release puede incluir `CHANGELOG.md`, `specs/INDEX.md` y el frontmatter de la spec, por decisión del propietario.
  - (d) `docs/Flujo_de_Trabajo_Git.md` aclara que, cuando un release combina correcciones y adiciones derivadas de ellas, el incremento lo decide la naturaleza dominante del conjunto y lo autoriza el propietario.
- **Decisión:** Concreción de RF-006 en `plan.md` (DEC-004) y en la tarea T-003. Sin cambio de requisitos. Ver «Decisiones de negocio» sobre la prioridad de versiones.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** RF-004 exige que la solicitud de `sdd` incluya la etapa, pero no fija el literal con el que se indica.
- **Pregunta:** ¿Se mantiene el literal «Etapa:» en la solicitud de `sdd`?
- **Respuesta:** Sí. Es el literal vigente desde la compuerta G4 de SPEC-002.
- **Decisión:** La solicitud de `documenter` usa el mismo literal (`plan.md`, interfaz de solicitud). Sin cambio de requisitos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005 «Escritura en .opencode/agents/»

- **Descripción:** El protocolo (§10) describe a `coder` como escritor de `src/`, `tests/`, `tools/` y `tasks.md`, pero la configuración técnica de `coder` le permite escribir en `.opencode/`. T-001 y T-002 escriben en `.opencode/agents/`, así que su ejecutor no estaba definido.
- **Pregunta:** ¿Quién ejecuta T-001 y T-002?
- **Respuesta:** Se autoriza a `coder` como excepción explícita para `.opencode/agents/`, registrada en esta clarificación. No se modifica el protocolo en esta spec.
- **Decisión:** Excepción de ejecución, desarrollada en `plan.md` (DEC-006). Sin cambio de requisitos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006 «Endurecimiento de documenter»

- **Descripción:** Los permisos de AMB-002 no restringen la ejecución de comandos de shell. Un agente de edición podría escribir archivos fuera de su alcance mediante un comando.
- **Pregunta:** ¿Debe `documenter` poder ejecutar comandos de shell, y cuál es su descripción aprobada?
- **Respuesta:** `documenter` añade la regla general `shell *` denegada, de modo que solo edita archivos. La descripción aprobada es: «Aplica correcciones editoriales y normativas en docs/ y AGENTS.md. Invocable por sdd como subagente. No toca código ni requisitos.»
- **Decisión:** Endurecimiento de permisos, desarrollado en `plan.md` (DEC-001). Sin cambio de requisitos: la denegación de shell limita el medio de escritura y no altera RF-002 ni CB-002.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007 «Fila de documenter en §10»

- **Descripción:** La reauditoría (BRE-02) detectó que la fila de `documenter` en la tabla de agentes del protocolo (§10) no estaba cubierta por ningún RF ni CA.
- **Pregunta:** ¿Se mantiene la fila de `documenter` en la tabla de agentes del protocolo?
- **Respuesta:** Sí. El propietario ratificó la fila el 2026-11-13. La tabla debe listar el rol nuevo.
- **Decisión:** Se mantiene. Queda registrada como parte de la corrección normativa de RF-006. Sin cambio de requisitos.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Ninguno. Los casos borde existentes (CB-001 a CB-003) cubren las situaciones detectadas en esta clarificación.

## Parches aplicados a `spec.md`

- [x] Frontmatter: `status: clarified` y `version: 0.3.0`.
- [x] Sección «Aprobaciones»: G1 registrada como aprobada por el propietario el 2026-11-13.
- [x] Historial de cambios: fila 0.3.0 «Aprobación G1 y clarificación».
- [x] AMB-005: sección «Actores y permisos», entrada de `coder`, registra la excepción de escritura en `.opencode/agents/` para T-001 y T-002.
- [x] AMB-006: sección «Actores y permisos», entrada de `documenter`, registra que no puede ejecutar comandos de shell.
- [x] Frontmatter: `version: 0.5.0`; historial: fila 0.5.0 «Decisiones del propietario AMB-005 y AMB-006».
- [x] AMB-007: la ratificación de la fila de `documenter` en §10 queda registrada en el historial de `spec.md` (0.7.0). La fila ya está aplicada en el protocolo por T-003, así que no requiere cambio de texto en `spec.md`.

## Decisiones de negocio

- Los requisitos RF-001 a RF-006, RNF-001 a RNF-003 y CB-001 a CB-003 no cambian en esta etapa.
- Se mantiene la prioridad de versiones del flujo Git (`MAJOR > MINOR > PATCH` para cambios mixtos). La «naturaleza dominante» de AMB-003 (d) se entiende como esa prioridad.
- El commit de release puede incluir el registro de cambios, el índice de specs y el frontmatter de la spec, siempre con autorización del propietario.
