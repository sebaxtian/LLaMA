---
id: SPEC-001
title: Fixture cobertura completa
status: draft
version: 0.1.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/validacion-g4
release: ""
---

# Fixture cobertura completa

## Contexto y objetivo

Caso de prueba: cada RF y CB aparece en alguna línea «Cubre:».

## Requisitos funcionales

### RF-001
CUANDO se valida la spec, el sistema DEBE comprobar la cobertura del requisito.

### RF-002
CUANDO se valida la spec, el sistema DEBE comprobar la cobertura del segundo requisito.

## Casos borde

### CB-001
SI un caso borde no tiene criterio, ENTONCES el sistema DEBE informarlo.

## Criterios de aceptación

### CA-001
DADO un RF cubierto, CUANDO se valida, ENTONCES no se emite advertencia para ese RF.
Cubre: RF-001.

### CA-002
DADO un RF y un CB cubiertos, CUANDO se valida, ENTONCES no se emite advertencia para ellos.
Cubre: RF-002, CB-001.

## Aprobaciones

- [ ] G1: aprobación del propietario.
