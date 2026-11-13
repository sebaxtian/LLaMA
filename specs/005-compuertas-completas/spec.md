---
id: SPEC-005
title: Compuertas completas y deuda residual
status: validated
version: 0.5.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/compuertas-completas
release: ""
supersedes: ""
superseded_by: ""
---

# Compuertas completas y deuda residual

## Contexto y objetivo

Las auditorías de SPEC-003 y SPEC-004 dejaron pendientes debilidades del validador determinista y de la descripción del protocolo operativo:

- La compuerta G3 (fin de Implement) no comprueba que todas las tareas estén completadas.
- La matriz de trazabilidad de un reporte de validación solo rechaza algunos estados no superados y no detecta celdas compuestas.
- La comprobación de Git compara la rama declarada también en especificaciones `released` o `superseded`, cuya rama puede haber sido eliminada tras la integración.
- SPEC-001 no declara sus líneas de cobertura, por lo que el validador emite advertencias sobre ella.
- El protocolo describe al agente `sdd` como de «solo lectura», aunque sus registros Git de artefactos requieren escritura.

El objetivo es que cada compuerta aplicable se compruebe sin huecos conocidos, que los reportes históricos sigan siendo válidos y que el protocolo describa con precisión la capacidad de escritura de `sdd`. Esta spec cierra la deuda residual del validador y aplica dos mantenimientos menores (RF-004 y RF-005).

## Actores y permisos

- **Propietario (Agent Sebaxtian):** aprueba la compuerta G1 de esta spec y, en etapas posteriores, las compuertas G4 y G6.
- **`planner`:** redacta esta spec y, en etapas posteriores, sus artefactos dentro de `specs/`.
- **`sdd`:** invoca el validador para cada compuerta, registra su código de salida y realiza el registro Git de los artefactos de control.
- **`coder`:** implementa las comprobaciones en etapas posteriores, una tarea por invocación.
- **`reviewer`:** emite el reporte de validación de esta spec.
- **Validador determinista:** comprueba las compuertas. No es un actor humano y no aprueba nada.

## Requisitos funcionales (EARS)

### RF-001

SI se solicita la compuerta G3 y alguna tarea de `tasks.md` no está marcada como completada (casilla `[x]` ausente), ENTONCES el validador DEBE devolver un error de validación.

### RF-002

SI una fila de la matriz de trazabilidad de un reporte de validación tiene un estado distinto de PASADO, incluidas las celdas compuestas que combinan PASADO con otro estado, ENTONCES el validador DEBE devolver un error de validación.

### RF-003

CUANDO se solicita la compuerta con comprobación de Git sobre una spec en estado `released` o `superseded`, el validador NO DEBE comparar la rama declarada en su frontmatter con la rama Git actual.

### RF-004

Cada criterio de aceptación de SPEC-001 DEBE declarar en su línea «Cubre:» los requisitos RF y CB que su reporte de validación registra como PASADO para ese criterio, sin cambiar el texto de ningún requisito ni de ningún criterio de aceptación. Las únicas modificaciones permitidas en el `spec.md` de SPEC-001 son las líneas «Cubre:» añadidas.

### RF-005

El protocolo operativo DEBE describir la capacidad de escritura del agente `sdd` como orquestador de solo lectura sobre artefactos y código, con permiso de registro de cambios Git (bookkeeping) de artefactos de control, y NO DEBE describirla como lectura absoluta.

## Requisitos no funcionales

### RNF-001

El validador DEBE devolver código de salida `0` cuando no hay errores de validación, `1` cuando hay al menos un error de validación y `2` ante un error de uso. Las advertencias NO DEBEN cambiar el código de salida.

### RNF-002

El validador DEBE usar únicamente la biblioteca estándar del lenguaje en que está implementado, sin dependencias externas.

### RNF-003

Las pruebas automatizadas del validador DEBEN ejecutarse con el mecanismo de pruebas incluido en la biblioteca estándar, sin dependencias externas ni instalación adicional.

## Casos borde

### CB-001

SI la celda de estado de una fila de la matriz de trazabilidad contiene «PASADO (con observación)», ENTONCES el validador NO DEBE considerar esa fila como no superada. Solo cuenta como superada una celda cuyo estado, tras normalizar mayúsculas y espacios, es PASADO seguido opcionalmente de una observación entre paréntesis. Una celda que combina PASADO con otro estado, como «PASADO / FALLADO», no es superada.

### CB-002

SI una spec en estado `released` tiene una rama declarada que ya no existe en el repositorio, ENTONCES el validador NO DEBE devolver un error por comparación de rama al solicitar la compuerta con comprobación de Git.

### CB-003

SI se valida SPEC-001 y SPEC-002 con la compuerta G4 después de implementar esta spec, ENTONCES ambas DEBEN devolver código de salida `0`.

## Fuera de alcance

- Modificar requisitos, criterios de aceptación o casos borde de SPEC-001 a SPEC-004. La única excepción es la línea «Cubre:» de SPEC-001 exigida por RF-004.
- Modificar los reportes de validación históricos (SPEC-001 a SPEC-004).
- Editar `opencode.jsonc`, los agentes, los comandos o los permisos de `.opencode/`.
- Cambiar el formato de los artefactos o los códigos de salida.
- Cambiar la comprobación de rama para estados distintos de `released` y `superseded`.
- Convertir en error la advertencia de cobertura RF/CB.
- Redactar `plan.md` o `tasks.md` en esta etapa.
- Aprobar esta spec. La aprobación G1 es exclusiva del propietario.

## Criterios de aceptación

### CA-001

DADO una spec con tareas en `tasks.md`, CUANDO se solicita la compuerta G3 y al menos una tarea no tiene la casilla `[x]`, ENTONCES el resultado contiene al menos un error de validación.

DADO una spec con todas sus tareas marcadas `[x]`, CUANDO se solicita la compuerta G3, ENTONCES el resultado no contiene errores relativos a las tareas.

Cubre: `RF-001`.

### CA-002

DADO un reporte con una fila cuya celda de estado es «PASADO (con observación)», CUANDO se valida con la compuerta G4, ENTONCES el resultado no contiene errores relativos a esa fila.

DADO un reporte con una fila cuya celda de estado es «FALLADO», «NO PASADO» o «PASADO / FALLADO», CUANDO se valida con la compuerta G4, ENTONCES el resultado contiene al menos un error de validación.

Cubre: `RF-002`, `CB-001`.

### CA-003

DADO una spec en estado `released` o `superseded` cuya rama declarada es distinta de la rama Git actual, CUANDO se valida con la compuerta con comprobación de Git, ENTONCES el resultado no contiene errores relativos a la rama.

DADO una spec en estado `released` cuya rama declarada ya no existe en el repositorio, CUANDO se valida con la compuerta con comprobación de Git, ENTONCES el resultado no contiene errores relativos a la rama.

Cubre: `RF-003`, `CB-002`.

### CA-004

DADO el archivo `spec.md` de SPEC-001, CUANDO se comparan sus criterios CA-001 a CA-005 con su reporte de validación, ENTONCES cada criterio tiene una línea «Cubre:» con los RF y CB que el reporte registra como PASADO para ese criterio, y el texto de sus requisitos y criterios es idéntico a la versión 0.3.0 salvo las líneas «Cubre:» añadidas.

DADO el archivo `spec.md` de SPEC-001 con esas líneas, CUANDO se valida, ENTONCES el resultado no contiene advertencias de cobertura RF/CB.

Cubre: `RF-004`.

### CA-005

DADO el protocolo operativo, CUANDO se consulta la tabla de agentes y permisos, ENTONCES la capacidad de escritura de `sdd` se describe como registro de cambios Git (bookkeeping) y no aparece como «solo lectura» sin matiz.

Cubre: `RF-005`.

### CA-006

DADO los reportes de validación de SPEC-001 y SPEC-002, CUANDO se valida cada spec con la compuerta G4, ENTONCES el código de salida es `0` y el resultado no contiene errores de validación.

DADO el validador, CUANDO se solicita una validación correcta, una validación con error de validación y una invocación con error de uso, ENTONCES devuelve `0`, `1` y `2` respectivamente.

DADO el validador, CUANDO se ejecutan sus pruebas automatizadas, ENTONCES todas pasan con el mecanismo de pruebas de la biblioteca estándar, y el código del validador solo importa módulos de la biblioteca estándar.

Cubre: `CB-003`, `RNF-001`, `RNF-002`, `RNF-003`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)
- [x] G4: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial en la etapa Specify |
| 0.2.0 | 2026-11-13 | Aprobación G1 y clarificación (AMB-001 a AMB-003); precisiones en RF-004, RF-005 y CB-001 |
| 0.3.0 | 2026-11-13 | Plan (DEC-001 a DEC-006) y desglose de tareas (T-001 a T-009) |
| 0.4.0 | 2026-11-13 | Implementación de compuertas completas |
| 0.5.0 | 2026-11-13 | G4 aprobada con dictamen CONVERGIDO |
