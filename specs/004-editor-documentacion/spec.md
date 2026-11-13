---
id: SPEC-004
title: Subagente documenter para correcciones normativas
status: validated
version: 0.8.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/editor-documentacion
release: ""
supersedes: ""
superseded_by: ""
---

# Subagente documenter para correcciones normativas

## Contexto y objetivo

El proyecto separa los permisos de escritura por agente para cumplir el principio de menor privilegio. Como consecuencia, ningún agente que puede lanzar subagentes tiene permiso para escribir en la documentación normativa del proyecto:

- El agente de planificación solo puede escribir en las especificaciones.
- El agente de implementación tiene denegada la escritura en la documentación.
- El agente orquestador no puede escribir en ningún archivo.

Esta carencia impide corregir la deuda O-02 registrada en la revisión de SPEC-002. Esa deuda consiste en dos contradicciones normativas:

- El protocolo SDD indica, en su sección de aprobaciones, que en la compuerta G4 «el propietario autoriza la implementación». La regla debe decir que el propietario aprueba la implementación validada.
- El flujo Git limita el commit de preparación de un release a un único archivo de registro de cambios y no documenta la excepción de contabilidad que el propietario autorizó: actualizar, en el mismo commit, el registro de cambios, el índice de specs y el estado de la spec.

El objetivo de esta spec es incorporar un subagente `documenter` con permisos de escritura limitados a la documentación del proyecto y al archivo de reglas operativas para agentes. El agente `sdd` debe poder lanzarlo para aplicar correcciones editoriales o normativas que no alteren requisitos, comportamiento ni código.

El alcance de esta spec incluye la aplicación efectiva de O-02 mediante `documenter`, que es el motivo de crear el subagente. La corrección de O-02 se exige en RF-006 y se verifica en CA-006.

## Actores y permisos

- **Propietario (Agent Sebaxtian):** aprueba la compuerta G1 de esta spec y decide cuándo se aplica cada corrección normativa.
- **`sdd`:** orquestador. Puede lanzar `documenter` y debe incluir en cada solicitud el identificador de la spec, la etapa y el resultado esperado.
- **`documenter`:** subagente de correcciones. Puede escribir en la documentación del proyecto y en el archivo de reglas operativas para agentes. No puede escribir en ningún otro archivo, no puede ejecutar comandos de shell ni lanzar subagentes.
- **`coder`:** sin cambios de permisos de configuración en esta spec. Ejecuta T-001 y T-002 con la excepción de escritura en `.opencode/agents/` (AMB-005).
- **`planner`, `reviewer`:** sin cambios de permisos en esta spec.

## Requisitos funcionales (EARS)

### RF-001

El agente `sdd` DEBE poder lanzar un subagente `documenter`.

### RF-002

El agente `documenter` DEBE poder editar los documentos de la documentación del proyecto y el archivo de reglas operativas para agentes, y NO DEBE poder editar ningún otro archivo.

### RF-003

El agente `documenter` NO DEBE poder lanzar subagentes.

### RF-004

CUANDO el agente `sdd` lance `documenter`, la solicitud DEBE incluir el identificador de la spec, la etapa en curso y el resultado esperado.

### RF-005

El agente `documenter` DEBE aplicar únicamente correcciones editoriales (erratas, formato o enlaces) y correcciones normativas que alineen un documento con otro de mayor rango, sin alterar requisitos, comportamiento ni código.

### RF-006

CUANDO se aplique la corrección normativa pendiente, `documenter` DEBE alinear el protocolo operativo y el archivo de reglas para que la compuerta G4 exprese la aprobación de la implementación validada, y DEBE documentar la excepción de contabilidad del commit de release.

## Requisitos no funcionales

### RNF-001

La declaración de permisos del agente `documenter` DEBE ser una lista ordenada en la que las reglas generales preceden a las excepciones.

### RNF-002

Los cambios aplicados en esta spec DEBEN registrarse en el registro de cambios del proyecto bajo la sección «Unreleased».

### RNF-003

Al editar un archivo, el agente `documenter` DEBE conservar su final de línea CRLF y su salto de línea final.

## Casos borde

### CB-001

SI una corrección exige cambiar requisitos, comportamiento o código, ENTONCES el agente `documenter` DEBE detenerse sin editar el archivo y reportar el motivo al orquestador.

### CB-002

SI el archivo objetivo de una edición no pertenece a la documentación del proyecto ni es el archivo de reglas operativas para agentes, ENTONCES la edición DEBE quedar denegada.

### CB-003

SI el agente `documenter` intenta lanzar un subagente, ENTONCES la operación DEBE quedar denegada.

## Fuera de alcance

- Modificar la configuración de OpenCode ni el archivo de servidores MCP.
- Modificar `specs/` distinto de esta spec, `src/`, `tools/` o `tests/`.
- Cambiar requisitos, criterios o casos borde de otras specs.
- Cambiar los permisos de `planner`, `coder` o `reviewer`.
- Redactar `clarify.md`, `plan.md` o `tasks.md` en esta etapa.
- Aprobar esta spec. La aprobación G1 es exclusiva del propietario.

## Criterios de aceptación

### CA-001

DADO el agente `sdd` en una sesión, CUANDO solicita lanzar `documenter`, ENTONCES el lanzamiento se inicia sin denegación de permisos.

Cubre: `RF-001`.

### CA-002

DADO el agente `documenter`, CUANDO intenta editar un documento de la documentación del proyecto o el archivo de reglas operativas para agentes, ENTONCES la edición se completa.

DADO el agente `documenter`, CUANDO intenta editar cualquier otro archivo, ENTONCES la edición queda denegada.

Cubre: `RF-002`, `CB-002`, `RNF-001`.

### CA-003

DADO el agente `documenter` en una tarea, CUANDO intenta lanzar un subagente, ENTONCES la operación queda denegada.

Cubre: `RF-003`, `CB-003`.

### CA-004

DADO una solicitud de `sdd` para lanzar `documenter`, CUANDO se revisa su contenido, ENTONCES incluye un identificador con formato `SPEC-NNN`, el nombre de la etapa en curso y una descripción del resultado esperado.

Cubre: `RF-004`.

### CA-005

DADO una corrección que exige cambiar un requisito, un comportamiento o código, CUANDO la evalúa el agente `documenter`, ENTONCES no edita ningún archivo y reporta el motivo al orquestador.

DADO una corrección editorial o normativa aplicada por el agente `documenter`, CUANDO se revisa el archivo editado, ENTONCES conserva el final de línea CRLF y el salto de línea final, y el cambio aparece en la sección «Unreleased» del registro de cambios.

Cubre: `RF-005`, `CB-001`, `RNF-002`, `RNF-003`.

### CA-006

DADO `documenter` habilitado, CUANDO aplica la corrección normativa, ENTONCES el protocolo y las reglas operativas describen G4 como aprobación de la implementación validada, y el flujo de release admite el registro de la especificación y del índice junto al registro de cambios.

Cubre: `RF-006`, `CB-001`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
- [x] G4: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial en la etapa Specify |
| 0.2.0 | 2026-11-13 | RF-006 y CA-006 para aplicar O-02 |
| 0.3.0 | 2026-11-13 | Aprobación G1 y clarificación |
| 0.4.0 | 2026-11-13 | Plan y tareas |
| 0.5.0 | 2026-11-13 | Decisiones del propietario AMB-005 y AMB-006 |
| 0.6.0 | 2026-11-13 | Implementación del subagente documenter y de O-02 |
| 0.7.0 | 2026-11-13 | Ratificación de la fila de documenter en §10 y cierre de BRE-01 |
| 0.8.0 | 2026-11-13 | G4 aprobada con dictamen CONVERGIDO |
