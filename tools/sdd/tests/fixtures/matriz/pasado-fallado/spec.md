---
id: SPEC-001
title: Fixture matriz pasado-fallado
status: tasked
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/validacion-g4
release: ""
---

# Fixture matriz pasado-fallado

## Contexto y objetivo

Caso de prueba: reporte de validación con una tabla de trazabilidad.

## Requisitos funcionales

### RF-001
CUANDO se valida la compuerta G4, el sistema DEBE evaluar la celda de estado de cada fila de la matriz.

## Casos borde

### CB-001
SI una celda de estado contiene una observación, ENTONCES el sistema DEBE aplicar la regla de superación.

## Criterios de aceptación

### CA-001
DADO un reporte con una fila por requisito, CUANDO se valida con G4, ENTONCES cada fila se evalúa por su estado.

Cubre: `RF-001`, `CB-001`.

## Aprobaciones

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
