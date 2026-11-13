---
id: SPEC-001
title: Fixture fila FALLADO
status: implemented
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/validacion-g4
release: ""
---

# Fixture fila FALLADO

## Contexto y objetivo

Caso de prueba: una fila de la matriz está en FALLADO y debe producir error.

## Requisitos funcionales

### RF-001
CUANDO se valida la compuerta G4, el sistema DEBE evaluar el reporte de validación.

## Casos borde

### CB-001
SI el reporte no existe, ENTONCES el sistema DEBE informar la ausencia.

## Criterios de aceptación

### CA-001
DADO un reporte, CUANDO se valida, ENTONCES el resultado se registra.

## Aprobaciones

- [ ] G1: aprobación del propietario.
