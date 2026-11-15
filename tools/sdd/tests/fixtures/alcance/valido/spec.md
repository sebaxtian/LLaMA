---
id: SPEC-013
title: Fixture del alcance de la referencia a la spec
status: implementing
version: 0.1.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/reauditoria-cierre
release: ""
supersedes: ""
superseded_by: ""
---

# Fixture del alcance de la referencia a la spec

## Contexto y objetivo

Caso de prueba del alcance de la comprobación de la cadena de la spec en los commits.

## Requisitos funcionales

### RF-001

CUANDO se valida el corpus, el sistema DEBE comprobar la cadena de la spec en los commits del alcance.

## Casos borde

### CB-001

SI el alcance resulta vacío, ENTONCES el sistema DEBE informar la comprobación como no aplicable.

## Criterios de aceptación

### CA-001

DADO el alcance de commits, CUANDO se valida, ENTONCES se comprueba la cadena de la spec.
Cubre: RF-001, CB-001.

## Aprobaciones

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-14)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado sin casillas pendientes |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | línea de G1 firmada y `plan.md` escrito |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` con los ocho campos |
| 2026-11-14 | T4 | `tasked` | `implementing` | orquestador | verificación de G2 registrada |
