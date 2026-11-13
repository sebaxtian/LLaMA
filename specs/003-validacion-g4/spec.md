---
id: SPEC-003
title: Validación estricta de la compuerta G4
status: released
version: 0.6.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/validacion-g4
release: "v0.3.1"
supersedes: ""
superseded_by: ""
---

# Validación estricta de la compuerta G4

## Contexto y objetivo

La compuerta G4 (fin de Validate) exige que el reporte de validación converja al 100 %. El validador determinista del protocolo es el árbitro de esa compuerta. En su versión actual presenta cuatro debilidades:

- Acepta cualquier reporte que contenga la palabra «CONVERGIDO», incluida la forma negativa «NO CONVERGIDO».
- No detecta filas de la matriz de trazabilidad en estado no PASADO, porque su comprobación no reconoce la forma real de la tabla.
- No comprueba que cada requisito RF o CB esté cubierto por al menos un criterio de aceptación (CA).
- No exige el reporte cuando se solicita la compuerta G4.

Estas debilidades quedaron registradas como O-01 y B-05 en la revisión de SPEC-002. Esta spec las corrige.

El objetivo es que una compuerta G4 solo supere la validación cuando el reporte tiene marcada la casilla «[x] CONVERGIDO», sin filas en estado FALLADO o NO PASADO, y que la cobertura RF/CB → CA sea visible en cada validación. La spec no cambia el formato de los artefactos ni los códigos de salida.

Regla de lectura del dictamen: una casilla está marcada cuando aparece como «[x]». El texto en prosa del reporte no determina el dictamen.

## Actores y permisos

- **Propietario (Agent Sebaxtian):** aprueba la compuerta G1 de esta spec y la compuerta G4 de la implementación.
- **`planner`:** redacta esta spec y, en etapas posteriores, sus artefactos dentro de `specs/`.
- **`sdd`:** invoca el validador antes de cada compuerta y registra su código de salida.
- **`coder`:** implementa los cambios en etapas posteriores, una tarea por invocación.
- **`reviewer`:** emite el reporte de validación de la spec.
- **Validador determinista:** comprueba las compuertas. No es un actor humano y no aprueba nada.

## Requisitos funcionales (EARS)

### RF-001

SI la compuerta G4, G5 o G6 se solicita y el reporte de validación de la spec no existe, ENTONCES el validador DEBE devolver un error de validación.

### RF-002

SI la casilla «[x] NO CONVERGIDO» está marcada en el dictamen del reporte, o la casilla «[x] CONVERGIDO» no está marcada, ENTONCES el validador DEBE devolver un error de validación.

### RF-003

SI la matriz de trazabilidad del reporte contiene una fila con estado FALLADO o NO PASADO, ENTONCES el validador DEBE devolver un error de validación.

### RF-004

SI un requisito RF o CB definido en `spec.md` no aparece en la línea «Cubre:» de ningún criterio de aceptación, ENTONCES el validador DEBE emitir una advertencia que identifique ese requisito.

### RF-005

CUANDO se valida una spec cuyo estado es anterior a `validated` y no tiene reporte de validación, el validador NO DEBE emitir un error por la ausencia del reporte.

## Requisitos no funcionales

### RNF-001

El validador DEBE devolver código de salida `0` cuando no hay errores de validación, `1` cuando hay al menos un error de validación y `2` ante un error de uso. Las advertencias NO DEBEN cambiar el código de salida.

### RNF-002

El validador DEBE usar únicamente la biblioteca estándar del lenguaje en que está implementado, sin dependencias externas.

### RNF-003

Las pruebas automatizadas del validador DEBEN ejecutarse con el mecanismo de pruebas incluido en la biblioteca estándar, sin dependencias externas ni instalación adicional.

## Casos borde

### CB-001

SI un reporte menciona «NO CONVERGIDO» solo en prosa y la casilla «[x] CONVERGIDO» está marcada, ENTONCES el validador NO DEBE tomar esa mención como dictamen negativo.

### CB-002

SI una spec en estado `draft` no tiene reporte de validación, ENTONCES el validador NO DEBE emitir un error por esa ausencia.

### CB-003

SI los reportes de validación de SPEC-001 y SPEC-002 se validan con la compuerta G4 después del endurecimiento, ENTONCES ambos DEBEN superar la compuerta sin errores de validación.

### CB-004

SI una spec en estado `validated` o `released` se valida sin indicar compuerta y no tiene reporte de validación, ENTONCES el validador DEBE devolver un error de validación.

## Fuera de alcance

- Convertir en error la advertencia de cobertura CA de RF-004. Requiere actualizar SPEC-001, que hoy no declara líneas «Cubre:».
- Cambiar el formato de `spec.md`, `clarify.md`, `plan.md`, `tasks.md` o `validation_report.md`.
- Cambiar los agentes, sus comandos o sus permisos.
- Modificar los reportes de SPEC-001 o SPEC-002.
- Redactar `clarify.md`, `plan.md` o `tasks.md` en esta etapa.
- Aprobar esta spec. La aprobación G1 es exclusiva del propietario.

## Criterios de aceptación

### CA-001

DADO una spec en estado `draft` sin reporte de validación, CUANDO se valida con la compuerta G4, ENTONCES el resultado contiene al menos un error de validación que indica la ausencia del reporte.

DADO una spec en estado `validated` sin reporte de validación, CUANDO se valida sin indicar compuerta, ENTONCES el resultado contiene al menos un error de validación.

Cubre: `RF-001`, `CB-004`.

### CA-002

DADO un reporte con la casilla «[x] NO CONVERGIDO» marcada, o con la casilla «[x] CONVERGIDO» sin marcar, CUANDO se valida con la compuerta G4, ENTONCES el resultado contiene al menos un error de validación.

DADO un reporte que menciona «NO CONVERGIDO» solo en prosa y tiene marcada la casilla «[x] CONVERGIDO», CUANDO se valida con la compuerta G4, ENTONCES el resultado no contiene errores relativos al dictamen.

Cubre: `RF-002`, `CB-001`.

### CA-003

DADO un reporte cuya matriz de trazabilidad contiene una fila con estado FALLADO o NO PASADO, CUANDO se valida con la compuerta G4, ENTONCES el resultado contiene al menos un error de validación.

Cubre: `RF-003`.

### CA-004

DADO una spec cuyo requisito RF o CB no aparece en ninguna línea «Cubre:», CUANDO se valida, ENTONCES el resultado contiene una advertencia que identifica ese requisito, y el código de salida no cambia por esa advertencia.

Cubre: `RF-004`.

### CA-005

DADO una spec en estado `draft` sin reporte de validación, CUANDO se valida sin compuerta o con la compuerta G1, ENTONCES el resultado no contiene errores por la ausencia del reporte.

DADO los reportes de SPEC-001 y SPEC-002, CUANDO se valida con la compuerta G4, ENTONCES el resultado no contiene errores de validación y el código de salida es `0`.

DADO el validador, CUANDO se ejecutan sus pruebas automatizadas, ENTONCES todas pasan con el mecanismo de pruebas de la biblioteca estándar, sin dependencias externas, y los códigos de salida cumplen RNF-001.

Cubre: `RF-005`, `CB-002`, `CB-003`, `RNF-001`, `RNF-002`, `RNF-003`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
- [x] G4: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial en la etapa Specify |
| 0.2.0 | 2026-11-13 | Aprobación G1 y clarificación |
| 0.3.0 | 2026-11-13 | Plan y tareas |
| 0.4.0 | 2026-11-13 | Implementación del validador estricto |
| 0.5.0 | 2026-11-13 | G4 aprobada con dictamen CONVERGIDO |
| 0.6.0 | 2026-11-13 | Release v0.3.1 autorizado por el propietario |
