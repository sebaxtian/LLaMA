---
id: SPEC-001
title: Fixture G3 con tarea pendiente
status: tasked
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/validacion-g3
release: ""
---

# Fixture G3 con tarea pendiente

## Contexto y objetivo

Caso de prueba: spec en estado tasked cuya tarea T-002 no está completada.

## Requisitos funcionales

### RF-001
CUANDO se solicita la compuerta G3, el sistema DEBE comprobar que todas las tareas están completadas.

## Casos borde

### CB-001
SI una tarea no está completada, ENTONCES el sistema DEBE informar del error.

## Criterios de aceptación

### CA-001
DADO una spec con tareas pendientes, CUANDO se solicita G3, ENTONCES el resultado contiene un error.

Cubre: `RF-001`, `CB-001`.

## Aprobaciones

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial del fixture |
