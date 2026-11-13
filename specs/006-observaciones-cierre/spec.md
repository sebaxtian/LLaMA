---
id: SPEC-006
title: Cierre de observaciones de documentación
status: implemented
version: 0.4.0
created: 2026-11-13
updated: 2026-11-13
owner: Agent Sebaxtian
branch: feat/observaciones-cierre
release: ""
supersedes: ""
superseded_by: ""
---

# Cierre de observaciones de documentación

## Contexto y objetivo

La validación de SPEC-005 (dictamen CONVERGIDO) dejó tres observaciones no bloqueantes. No alteran requisitos ni comportamiento, pero sí la exactitud de la documentación y la trazabilidad de decisiones ya tomadas:

- **Observación O-1 de SPEC-005 (exigida por la spec 005):** la fila de `sdd` en la tabla de agentes del protocolo operativo describe la lectura y el bookkeeping Git de artefactos de control, pero no usa la expresión exigida «orquestador de solo lectura sobre artefactos y código».
- **Memoria operativa incompleta:** la memoria operativa no enumera el agente `documenter` ni explica cómo consultar los agentes del proyecto. Durante la especificación se comprobó que el listado de agentes depende del directorio de trabajo: ejecutado fuera del repositorio, no muestra los agentes del proyecto.
- **Observación O-2 de SPEC-005 (AMB-001 de SPEC-005):** la regla de celda superada de AMB-001 quedó pendiente de confirmación explícita del propietario al revisar G1. Esa confirmación no consta en la clarificación de SPEC-005.

El objetivo es que la documentación describa con exactitud a `sdd` y a los agentes del proyecto, y que la clarificación de SPEC-005 registre la decisión confirmada, sin modificar ningún requisito ni comportamiento.

Restricción detectada: `documenter` solo puede editar documentación, y `planner` solo puede editar `specs/`; ninguno de los dos puede modificar la memoria operativa ni el registro de cambios. `coder` sí puede hacerlo, porque su permiso de edición cubre el resto de archivos salvo `specs/**` y `docs/**`. La asignación de ejecutores queda registrada en el desglose de tareas.

## Actores y permisos

- **Propietario (Agent Sebaxtian):** aprueba la compuerta G1 de esta spec, emite la confirmación de la regla de AMB-001 que registra RF-003 y decide cualquier excepción de permisos que surja durante la implementación.
- **`planner`:** redacta esta spec y, en etapas posteriores, sus artefactos dentro de `specs/`.
- **`sdd`:** orquesta las etapas, invoca el validador y registra en Git los artefactos de control. No edita documentos ni código.
- **`documenter`:** aplica la corrección de la tabla de agentes del protocolo operativo (RF-001), dentro de su permiso sobre documentación.
- **`coder`:** aplica la actualización de la memoria operativa (RF-002) y la entrada del registro de cambios (RNF-002), dentro de su permiso de edición.
- **Registro en la clarificación de SPEC-005:** `planner` añade la confirmación de AMB-001 (RF-003), dentro de su permiso sobre `specs/`.
- **`reviewer`:** emite el reporte de validación de esta spec.
- **Validador determinista:** comprueba la estructura y la trazabilidad de la spec. No es un actor humano y no aprueba nada.

## Requisitos funcionales (EARS)

### RF-001

La tabla de agentes y permisos del protocolo operativo DEBE describir al agente `sdd` como «orquestador de solo lectura sobre artefactos y código» y DEBE limitar su registro de cambios Git (bookkeeping) a artefactos de control. NO DEBE describir esa capacidad como lectura sin matiz.

### RF-002

La memoria operativa DEBE enumerar los agentes `sdd`, `planner`, `coder`, `reviewer`, `explore` y `documenter`, e indicar que `explore` es un subagente integrado de OpenCode. DEBE indicar el comando que lista los agentes del proyecto y que ese comando debe ejecutarse con el directorio del repositorio como directorio de trabajo.

### RF-003

La clarificación de SPEC-005 DEBE registrar la confirmación explícita del propietario sobre la regla de celda superada de AMB-001: una celda es superada solo si, tras normalizar mayúsculas y espacios, su estado es PASADO seguido opcionalmente de una observación entre paréntesis. El registro DEBE indicar la fecha y el responsable, y DEBE marcar como confirmado el punto pendiente de AMB-001. La confirmación DEBE provenir del propietario; el ejecutor NO DEBE registrarla por iniciativa propia.

## Requisitos no funcionales

### RNF-001

Los archivos modificados por esta spec DEBEN conservar finales de línea CRLF y terminar con salto de línea final.

### RNF-002

Cada cambio de esta spec DEBE registrarse en el registro de cambios bajo la sección Unreleased, con una entrada que cite SPEC-006.

### RNF-003

Esta spec NO DEBE alterar requisitos, criterios de aceptación ni casos borde de otras specs, ni código, ni la configuración de agentes, comandos o permisos. Fuera de esta spec, la única modificación permitida es el registro de RF-003 en la clarificación de SPEC-005, además de las entradas de registro de specs y de registro de cambios.

## Casos borde

### CB-001

SI la corrección de una observación exige cambiar un requisito, el comportamiento de código, agentes, comandos o permisos, ENTONCES el ejecutor DEBE detenerse, NO DEBE modificar ningún archivo y DEBE reportar la observación al propietario como pendiente.

### CB-002

SI el comando de consulta de agentes se ejecuta sin el directorio del repositorio como directorio de trabajo, ENTONCES devuelve los agentes del directorio por defecto y no los del proyecto, y la memoria operativa DEBE advertir ese requisito de ejecución.

## Fuera de alcance

- Modificar requisitos, criterios de aceptación o casos borde de SPEC-001 a SPEC-005, salvo el registro de RF-003.
- Modificar los reportes de validación históricos, incluido el de SPEC-005. Las observaciones quedan registradas allí sin cambios.
- Editar agentes, comandos, permisos o configuración de `.opencode/` y `opencode.jsonc`.
- Ampliar los permisos de `documenter`, `coder` o `planner` para editar la memoria operativa o el registro de cambios. Ese cambio requeriría una spec propia.
- Cambiar el validador, sus códigos de salida o sus reglas de estado.
- Modificar el comportamiento del comando de consulta de OpenCode o proponer otro comando.
- Redactar `clarify.md`, `plan.md` o `tasks.md` de esta spec en la etapa Specify.
- Aprobar G1, G4 o G6. La confirmación de AMB-001 y todas las aprobaciones son exclusivas del propietario.

## Criterios de aceptación

### CA-001

DADO el protocolo operativo, CUANDO se consulta la tabla de agentes y permisos, ENTONCES la fila de `sdd` contiene la expresión «orquestador de solo lectura sobre artefactos y código» y limita su registro Git a artefactos de control.

Cubre: `RF-001`.

### CA-002

DADO la memoria operativa, CUANDO se revisa su sección de agentes, ENTONCES enumera `sdd`, `planner`, `coder`, `reviewer`, `explore` y `documenter`, e indica que el comando `opencode debug agents` debe ejecutarse con el directorio de trabajo en la raíz del repositorio.

DADO el comando `opencode debug agents` ejecutado con el directorio de trabajo en la raíz del repositorio, CUANDO devuelve su lista de agentes, ENTONCES incluye `sdd`, `planner`, `coder`, `reviewer` y `documenter`.

DADO el comando `opencode debug agents` ejecutado con otro directorio de trabajo, CUANDO devuelve su lista de agentes, ENTONCES no incluye `sdd`, `planner`, `coder`, `reviewer` ni `documenter`, y la memoria operativa advierte ese requisito.

Cubre: `RF-002`, `CB-002`.

### CA-003

DADO la clarificación de SPEC-005, CUANDO se revisa el registro de AMB-001, ENTONCES contiene la confirmación explícita del propietario sobre la regla de celda superada, con fecha y responsable, y el punto pendiente figura como confirmado.

DADO que el propietario no ha emitido esa confirmación, CUANDO se ejecuta el registro, ENTONCES no se escribe ninguna confirmación en la clarificación de SPEC-005.

Cubre: `RF-003`.

### CA-004

DADO una corrección que exige cambiar un requisito, el comportamiento de código, agentes, comandos o permisos, CUANDO el ejecutor la analiza, ENTONCES se detiene, no modifica ningún archivo y reporta la observación como pendiente al propietario.

DADO el conjunto de archivos modificados por esta spec, CUANDO se revisan sus finales de línea, ENTONCES conservan CRLF y terminan con salto de línea final.

DADO el registro de cambios, CUANDO se revisa tras la implementación, ENTONCES contiene una entrada bajo Unreleased que cita SPEC-006.

DADO la comparación con la rama `main`, CUANDO se revisa el conjunto de cambios, ENTONCES no hay diferencias en requisitos, criterios ni casos borde de otras specs, ni en código, salvo el registro de RF-003.

Cubre: `CB-001`, `RNF-001`, `RNF-002`, `RNF-003`.

## Aprobaciones

<!-- Solo el propietario puede rellenar esta sección. -->

- [x] G1: - Approved by: Agent Sebaxtian (2026-11-13)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-13 | Redacción inicial en la etapa Specify |
| 0.2.0 | 2026-11-13 | Aprobación G1 y clarificación (AMB-001 a AMB-003); corrección de la restricción de permisos de `coder` |
| 0.3.0 | 2026-11-13 | Plan (DEC-001 a DEC-003) y desglose de tareas (T-001 a T-005) |
| 0.4.0 | 2026-11-13 | Implementación de cierre de observaciones |
