---
id: SPEC-001
title: Fixture validated con rama distinta
status: validated
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/rama-declarada
release: ""
---

# Fixture validated con rama distinta

## Contexto y objetivo

Caso de prueba: spec validada cuya rama declarada no coincide con la rama Git actual.

## Requisitos funcionales

### RF-001
CUANDO se solicita la compuerta con comprobación de Git, el sistema DEBE comparar la rama declarada con la rama actual en specs no integradas.

## Casos borde

### CB-001
SI la rama declarada no coincide con la actual, ENTONCES el sistema DEBE devolver un error de rama.

## Criterios de aceptación

### CA-001
DADO una spec validated con rama distinta, CUANDO se valida con Git, ENTONCES el resultado contiene un error de rama.

Cubre: `RF-001`, `CB-001`.

## Aprobaciones

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
