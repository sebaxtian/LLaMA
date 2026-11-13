---
id: SPEC-001
title: Fixture released con rama eliminada
status: released
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/rama-eliminada
release: "v0.1.0"
---

# Fixture released con rama eliminada

## Contexto y objetivo

Caso de prueba: spec integrada cuya rama declarada ya no existe en el repositorio.

## Requisitos funcionales

### RF-001
CUANDO se solicita la compuerta con comprobación de Git, el sistema DEBE omitir la comparación de rama en specs released.

## Casos borde

### CB-001
SI la rama declarada ya no existe, ENTONCES el sistema NO DEBE devolver un error de rama.

## Criterios de aceptación

### CA-001
DADO una spec released con rama eliminada, CUANDO se valida con Git, ENTONCES el resultado no contiene errores de rama.

Cubre: `RF-001`, `CB-001`.

## Aprobaciones

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
