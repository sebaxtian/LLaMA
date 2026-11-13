---
id: SPEC-002
title: Orquestación de subagentes SDD
status: implemented
version: 0.4.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/orquestacion-subagentes-sdd
release: ""
supersedes: ""
superseded_by: ""
---

# Orquestación de subagentes SDD

## Contexto y objetivo

El agente orquestador `sdd` debe conducir el ciclo SDD completo delegando en los agentes especializados. En la configuración vigente, `planner` y `coder` solo pueden actuar como agentes primarios, por lo que `sdd` no puede lanzarlos como subagentes y el ciclo solo avanza si la persona cambia de agente de forma manual. El objetivo es habilitar la delegación desde `sdd` con permisos mínimos, verificación de compuertas antes de cada lanzamiento y trazabilidad de los resultados en los artefactos de la spec.

## Actores y permisos

- **Propietario:** aprueba las compuertas G1, G4 y G6 y autoriza releases.
- **`sdd`:** diagnostica estado, verifica compuertas y lanza subagentes; no edita artefactos ni código.
- **`planner`:** redacta `spec.md`, `clarify.md`, `plan.md` y `tasks.md` dentro de `specs/`.
- **`coder`:** implementa una única tarea aprobada por invocación.
- **`reviewer`:** audita la convergencia y emite `validation_report.md`.

## Requisitos funcionales (EARS)

### RF-001

CUANDO el agente `sdd` inicia una etapa del ciclo que requiere un agente especializado, el sistema DEBE permitirle lanzar `planner`, `coder` o `reviewer` como subagente.

### RF-002

El agente `planner` DEBE poder ejecutarse como agente primario y como subagente.

### RF-003

El agente `coder` DEBE poder ejecutarse como agente primario y como subagente.

### RF-004

SI `sdd` intenta lanzar un subagente distinto de `planner`, `coder`, `reviewer` o `explore`, ENTONCES el sistema DEBE denegar el lanzamiento.

### RF-005

El agente `sdd` NO DEBE poder editar archivos del proyecto.

### RF-006

ANTES de lanzar un subagente, `sdd` DEBE verificar que la compuerta previa de esa etapa esté aprobada.

### RF-007

CUANDO `sdd` lanza un subagente, DEBE incluir en la solicitud el identificador de la spec, la etapa en curso y el resultado esperado.

## Requisitos no funcionales

### RNF-001

La configuración de permisos DEBE expresarse con la lista ordenada `permissions` de OpenCode V2, usando `action`, `resource` y `effect`, y DEBE situar las reglas generales antes de las excepciones.

### RNF-002

Los cambios de configuración DEBEN quedar registrados en `CHANGELOG.md` bajo `Unreleased` antes de publicar la release.

## Casos borde

### CB-001

SI `coder` se lanza sin aprobación G4, ENTONCES `sdd` DEBE detenerse y reportar el bloqueo.

### CB-002

SI un subagente se detiene por ambigüedad o por alcance no declarado, ENTONCES `sdd` DEBE registrar el bloqueo sin emitir resultados supuestos.

### CB-003

SI la compuerta previa no puede verificarse porque el validador devuelve un error de validación, ENTONCES `sdd` DEBE detenerse y reportar el error de validación.

## Fuera de alcance

- Cambios en los permisos de `reviewer`.
- Cambios en `opencode.jsonc`.
- Ejecución en paralelo de varios subagentes sobre la misma spec.
- Aprobación automática de compuertas.

## Criterios de aceptación

### CA-001

DADO el agente `sdd` activo, CUANDO se solicita la etapa Plan, ENTONCES `planner` está disponible como subagente y produce `plan.md`.

### CA-002

DADO el agente `sdd` activo, CUANDO se solicita la etapa Implement, ENTONCES `coder` está disponible como subagente.

### CA-003

DADO el agente `sdd` activo, CUANDO se intenta lanzar un agente no autorizado, ENTONCES el lanzamiento queda denegado.

### CA-004

DADO el agente `sdd` activo, CUANDO se intenta editar un archivo del proyecto, ENTONCES la edición queda denegada.

### CA-005

DADO `sdd` y una spec sin G4 aprobada, CUANDO se intenta lanzar `coder`, ENTONCES `sdd` detiene el flujo y reporta el bloqueo.

### CA-006

DADO `planner` y `coder` configurados para doble modo, CUANDO se invocan desde los comandos `sdd-*`, ENTONCES responden como agentes primarios.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial |
| 0.2.0 | 2026-11-13 | Aprobación G1 |
| 0.3.0 | 2026-11-13 | Clarificación, plan y tareas |
| 0.4.0 | 2026-11-13 | Implementación de la orquestación |