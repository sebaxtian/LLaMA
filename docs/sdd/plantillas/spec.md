---
id: SPEC-XXX
title: <título de la feature>
status: draft
version: 0.1.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: Agent Sebaxtian
branch: feat/<nombre>
release: ""
supersedes: ""
superseded_by: ""
---

# <Título de la feature>

*Plantilla de rango 5: norma de forma del artefacto `spec.md` de una spec de `specs/NNN-slug/`. Cada campo tiene una sola forma y cada sección se escribe una sola vez.*

## Contexto y objetivo

<Problema que resuelve y resultado esperado: qué, para qué y por qué. Sin detalles de implementación.>

## Actores y permisos

- **<Actor>:** <qué puede hacer y sobre qué>.

## Requisitos funcionales (EARS)

### RF-001

`CUANDO <evento>, el sistema DEBE <respuesta con número y unidad en cada umbral>.`

### RF-002

`El sistema DEBE <respuesta>.`

## Requisitos no funcionales

### RNF-001

`El sistema DEBE <atributo medible con número y unidad>.`

## Casos borde

### CB-001

`SI <condición límite>, ENTONCES el sistema DEBE <respuesta>.`

## Fuera de alcance

- <Lo que esta spec no cubre>.

## Criterios de aceptación

### CA-001

`DADO <precondición>, CUANDO <acción>, ENTONCES <resultado observable>.`

Cubre: `RF-001`, `CB-001`.

### CA-002

`DADO <precondición>, CUANDO <acción>, ENTONCES <resultado observable>.`

Cubre: `RF-002`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [ ] G1: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | YYYY-MM-DD | Redacción inicial |

<!-- Prohibiciones de esta plantilla: rutas de código, clases, SQL y comandos técnicos; casilla de G6; dos formas para un mismo campo. -->
