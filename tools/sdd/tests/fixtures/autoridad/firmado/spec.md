---
id: SPEC-010
title: Autoría con commit firmado
status: clarified
version: 0.1.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/mecanismo-control-sdd
release: ""
supersedes: ""
superseded_by: ""
---

# Autoría con commit firmado

## Contexto y objetivo

El commit que introduce la línea está firmado por una clave de la lista de firmantes autorizados.


## Requisitos funcionales

### RF-001
CUANDO se evalúa la spec, el sistema DEBE comprobar la condición descrita en el contexto.

## Casos borde

### CB-001
SI la condición no se cumple, ENTONCES el sistema DEBE registrar un hallazgo.

## Criterios de aceptación

### CA-001
DADO el fixture, CUANDO se valida, ENTONCES se comprueba su condición.
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

