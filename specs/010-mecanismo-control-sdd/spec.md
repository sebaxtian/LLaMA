---
id: SPEC-010
title: Mecanismo de control SDD verificable
status: validated
version: 0.5.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/mecanismo-control-sdd
release: ""
supersedes: ""
superseded_by: ""
---

# Mecanismo de control SDD verificable

## Contexto y objetivo

El informe `docs/sdd/auditoria_cumplimiento_sdd.md` emite veredicto global `NO CONFORME` y concentra en el bloque B2 los defectos del mecanismo de control. La base normativa v2, integrada por `SPEC-009`, ya fija la autoridad documental, la tabla de transiciones, las seis compuertas con su declarante y el registro único de aprobaciones. El mecanismo que ejecuta esas reglas no está alineado con ellas: la condición de entrada de Implement admite dos compuertas distintas, G3 se evalúa por tarea y también al cierre, la compuerta G4 se ejecuta antes de existir el reporte que ella misma exige, tres estados admitidos no tienen escritor, el registro de G4 se reparte entre dos artefactos, el validador no comprueba ninguna aprobación, la cobertura de requisitos solo produce advertencia, G5 y G6 comparten la verificación de G4, el modelo de estados no se comprueba, la relación de sucesión no se valida y el verde del validador se lee como conformidad del régimen sin cubrir compuertas ni transiciones.

Objetivo: fijar el contrato del mecanismo de control verificable que cierra los dieciséis hallazgos del bloque B2, de modo que cada compuerta tenga una sola condición de entrada, una sola evidencia, un solo declarante y una sola verificación, y que cada estado tenga un escritor, una transición admitida y un registro.

Resultado esperado: comandos con orden de ejecución declarado y sin circularidad; validador que comprueba la aprobación de G1, G4 y G6 contra la lista de firmantes y la firma del commit; cobertura de requisitos como error desde G2; tareas abiertas detectadas en la ejecución agregada; G5 y G6 con lógica propia; transiciones y sucesión comprobadas; historial de transiciones registrado; alcance exacto del validador impreso en cada ejecución y una prueba positiva y una negativa por comprobación nueva.

La feature se redacta con la base v2 vigente. No modifica la base normativa, no implementa los bloques B3 ni B4 del informe y no reescribe las specs publicadas. Un resultado favorable del validador acredita las comprobaciones que ejecuta y no sustituye la aprobación del propietario ni la conformidad del régimen.

El protocolo operativo v2 fija la tabla de transiciones, el registro único de G1, G4 y G6, la verificación por commit firmado y el alcance del validador: esta spec implementa esas reglas y no las modifica. El historial de transiciones se registra como subsección `### Historial de transiciones` dentro de la sección `## Historial de cambios`, de modo que la spec conserva las nueve secciones del contrato de rango 5.

### Trazabilidad con el informe de auditoría

| Hallazgo | Requisitos que lo resuelven | Criterios de aceptación |
|---|---|---|
| `AUD-011` | `RF-001` | `CA-001` |
| `AUD-012` | `RF-004` | `CA-003` |
| `AUD-013` | `RF-005` | `CA-004` |
| `AUD-014` | `RF-002`, `RF-003`, `RF-021` | `CA-002`, `CA-005` |
| `AUD-021` | `RF-006`, `RF-020` | `CA-006` |
| `AUD-031` | `RF-007`, `RF-010` | `CA-007` |
| `AUD-032` | `RF-011` | `CA-010` |
| `AUD-033` | `RF-012` | `CA-011` |
| `AUD-034` | `RF-008` | `CA-008` |
| `AUD-035` | `RF-009`, `RF-013`, `RF-014` | `CA-009`, `CA-012` |
| `AUD-051` | `RF-015` | `CA-013` |
| `AUD-052` | `RF-002`, `RF-003`, `RF-021` | `CA-002`, `CA-005` |
| `AUD-053` | `RF-016` | `CA-014` |
| `AUD-054` | `RF-017` | `CA-015` |
| `AUD-062` | `RF-010`, `RF-020` | `CA-006`, `CA-007` |
| `AUD-094` | `RF-018`, `RF-019`, `RNF-005` | `CA-016`, `CA-017`, `CA-019` |

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1, G4 y G6 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`; no delega la firma y no acepta una aprobación emitida por un agente.
- **Orquestador (`sdd`):** ejecuta el validador, verifica G2, G3 y G5, evalúa G4 después de la firma del propietario, escribe las transiciones `implementing`, `implemented` y `validated` y lanza los subagentes; no declara aprobaciones.
- **Agente `planner`:** redacta `spec.md`, `clarify.md`, `plan.md` y `tasks.md` y escribe las transiciones `clarified`, `planned` y `tasked`; no escribe estados de implementación ni líneas de aprobación.
- **Agente `coder`:** ejecuta tareas y transcribe su evidencia en `tasks.md`; no escribe el campo `status` de la spec.
- **Agente `reviewer`:** ejecuta el comando `/sdd-validate` y escribe `validation_report.md` con la matriz y el dictamen; no evalúa G4, no escribe casilla de aprobación y no escribe el estado `validated`.
- **Validador:** comprueba estructura, compuertas, transiciones y sucesión, declara su alcance y devuelve un código de salida; no acredita aprobación alguna.
- **Rol de auditoría:** lee la base y el mecanismo y produce su informe; no aprueba compuertas y su implementación en `.opencode/` corresponde al bloque B3.

## Requisitos funcionales (EARS)

### RF-001

`CUANDO se invoca el comando `/sdd-implement`, el sistema DEBE exigir la verificación G2 registrada sin hallazgos y el campo `status` de `spec.md` en `tasked`, y NO DEBE admitir G4 como condición de entrada.`

### RF-002

`CUANDO el comando `/sdd-implement` inicia la primera tarea, el sistema DEBE escribir `implementing` en el campo `status` de `spec.md` y DEBE añadir la fila de la transición T4 en la subsección `### Historial de transiciones`.`

### RF-003

`CUANDO el comando `/sdd-implement` cierra la última tarea pendiente con su evidencia transcrita y las pruebas en verde, el sistema DEBE escribir `implemented` en el campo `status` de `spec.md` y DEBE añadir la fila de la transición T5 en la subsección `### Historial de transiciones`.`

### RF-004

`El sistema DEBE evaluar G3 una sola vez, al cierre de la etapa Implement, y NO DEBE evaluarla por tarea.`

### RF-005

`CUANDO se ejecuta el comando `/sdd-validate`, el rol `reviewer` DEBE escribir `validation_report.md` y NO DEBE evaluar G4 ni escribir el estado `validated`; la evaluación de G4 DEBE ejecutarse después de que el reporte exista y de que el propietario firme la línea de aprobación en `spec.md`.`

### RF-006

`El reporte de validación NO DEBE contener casilla de aprobación ni registro de compuerta, y la aprobación de G4 DEBE registrarse solo en la sección de aprobaciones de `spec.md`.`

### RF-007

`CUANDO se evalúa G1, el validador DEBE exigir en `spec.md` la casilla de G1 marcada, con la forma `- [x] G1:` seguida de la cadena exacta `- Approved by: Agent Sebaxtian` y de una fecha en formato ISO, y NO DEBE declarar aprobada la compuerta si falta alguno de esos tres elementos.`

### RF-008

`CUANDO se evalúa G4, el validador DEBE exigir el dictamen `CONVERGIDO` marcado, cada fila de la matriz de trazabilidad en `PASADO` y la casilla de G4 marcada con la forma `- [x] G4:` seguida de la cadena exacta de aprobación y de una fecha en formato ISO en `spec.md`.`

### RF-009

`CUANDO se evalúa G6, el validador DEBE exigir la viñeta con la cadena exacta de aprobación dentro de la entrada del release en `CHANGELOG.md` y, cuando el componente MINOR del tag supere al del tag anterior en orden SemVer, DEBE exigir la referencia al informe de auditoría de conformidad en esa entrada.`

### RF-010

`CUANDO se evalúa la aprobación de G1, G4 o G6, el validador DEBE localizar con `git log -S` el commit más reciente que introdujo la línea en el archivo correspondiente, DEBE verificar la firma de ese commit con `git verify-commit` y DEBE cotejar la clave firmante con `docs/sdd/firmantes_autorizados`, sin acceso a red.`

### RF-011

`A partir de G2, el validador DEBE tratar como error cada `RF` y cada `CB` de `spec.md` que no figure en una línea `Cubre:` de los criterios de aceptación, y NO DEBE emitir solo una advertencia.`

### RF-012

`CUANDO se ejecuta la validación agregada del validador, el sistema DEBE tratar como error cada tarea sin la casilla `Completada` marcada en las specs con estado `implemented`, `validated` o `released`.`

### RF-013

`CUANDO se evalúa G5, el validador DEBE exigir una integración con dos padres en `dev`, una ejecución del validador posterior a esa integración sin hallazgos y la ausencia de la rama de trabajo en las ramas locales y en las referencias remotas de seguimiento, y NO DEBE ejecutar consulta de red.`

### RF-014

`CUANDO se evalúa G6, el validador DEBE comprobar el tag anotado con tipo tag, con el mensaje `Release vX.Y.Z` y con el commit objetivo verificado, DEBE comparar el componente MINOR con el del tag anterior del listado local de tags para determinar si el release es menor, y DEBE exigir que `specs/INDEX.md` y `CHANGELOG.md` declaren el estado `released` y el identificador del release.`

### RF-015

`El validador DEBE comprobar que el estado escrito en `spec.md` es el destino de una transición admitida desde el estado de la última fila de la subsección `### Historial de transiciones`, y DEBE rechazar con código de salida 1 una transición no admitida.`

### RF-016

`El sistema DEBE registrar cada transición de estado en la subsección `### Historial de transiciones` de la sección `## Historial de cambios` de `spec.md`, con las columnas Fecha, Transición, Origen, Destino, Responsable y Evidencia, y NO DEBE admitir un cambio de estado sin la fila correspondiente.`

### RF-017

`El validador DEBE comprobar la reciprocidad entre `supersedes` y `superseded_by` de dos specs, DEBE exigir `superseded_by` en una spec con estado `superseded` y DEBE exigir el estado `superseded` en una spec que declara `superseded_by`.`

### RF-018

`El validador DEBE imprimir en cada ejecución la lista de comprobaciones ejecutadas y la lista de comprobaciones no verificadas, y NO DEBE presentar un resultado favorable como acreditación de conformidad del régimen ni de aprobación de compuerta.`

### RF-019

`Cada comprobación nueva del validador DEBE incorporarse con una prueba positiva y una prueba negativa en la suite de `tools/sdd/tests/`, y NO DEBE incorporarse sin ambas.`

### RF-020

`El validador DEBE rechazar una línea de aprobación escrita fuera de la ubicación única de su compuerta: G1 y G4 en `spec.md` y G6 en `CHANGELOG.md`.`

### RF-021

`CUANDO el propietario firma la aprobación de G4 con el reporte convergido, el orquestador DEBE escribir `validated` en `spec.md` y DEBE añadir la fila de la transición T6 en la subsección `### Historial de transiciones`.`

## Requisitos no funcionales

### RNF-001

`El validador DEBE devolver el mismo veredicto y el mismo código de salida ante dos ejecuciones consecutivas sobre la misma entrada.`

### RNF-002

`La ejecución agregada del validador DEBE completar en 60 segundos o menos sobre el corpus vigente en el equipo objetivo.`

### RNF-003

`El validador DEBE operar solo con la biblioteca estándar de Python 3 y NO DEBE realizar acceso a red.`

### RNF-004

`Cada hallazgo de la salida DEBE ocupar una línea con la severidad, la ruta del artefacto y la comprobación que lo produce.`

### RNF-005

`El validador NO DEBE escribir, mover ni eliminar archivos del repositorio durante la verificación.`

### RNF-006

`El validador DEBE aplicar la cláusula de legado a las specs publicadas `SPEC-001` a `SPEC-009` y NO DEBE devolver código de salida 1 por una comprobación incorporada con posterioridad a su publicación.`

## Casos borde

### CB-001

`SI la línea de aprobación existe y el commit que la introduce carece de firma que verifique, o su clave no figura en `docs/sdd/firmantes_autorizados`, ENTONCES el validador DEBE declarar la compuerta no aprobada con código de salida 1.`

### CB-002

`SI una compuerta registra líneas de aprobación en dos ubicaciones, ENTONCES el validador DEBE registrar un error de registro dual y NO DEBE declarar la compuerta superada.`

### CB-003

`SI `validation_report.md` contiene una casilla de aprobación, ENTONCES el validador DEBE registrar un error de contrato del reporte.`

### CB-004

`SI se evalúa una compuerta cuyo estado de origen no es el que la tabla de transiciones exige, ENTONCES el validador DEBE registrar un error y NO DEBE declarar la compuerta superada.`

### CB-005

`SI `supersedes` declara un identificador `SPEC-NNN` sin carpeta en `specs/`, ENTONCES el validador DEBE registrar un error de sucesión.`

### CB-006

`SI una spec declara `superseded_by` y no figura en estado `superseded`, ENTONCES el validador DEBE registrar un error de coherencia de estado.`

### CB-007

`SI una spec en estado `released` carece de la cadena exacta de aprobación de G6 en su entrada de `CHANGELOG.md`, ENTONCES el validador DEBE registrar un error y NO DEBE declarar G6 superada.`

### CB-008

`SI la validación agregada encuentra una tarea abierta en una spec con estado `implemented`, `validated` o `released`, ENTONCES el validador DEBE registrar un error con el identificador de la tarea.`

### CB-009

`SI se invoca el comando `/sdd-implement` con la spec en `tasked` y sin la verificación G2 registrada, ENTONCES el sistema DEBE detenerse sin escribir estado ni iniciar tarea.`

### CB-010

`SI el reporte de validación existe con el dictamen `NO CONVERGIDO` marcado, ENTONCES el validador DEBE declarar G4 no superada y la spec DEBE permanecer en `implemented`.`

### CB-011

`SI la subsección `### Historial de transiciones` no contiene fila para el estado escrito en `spec.md`, ENTONCES el validador DEBE registrar un error de trazabilidad de estado.`

### CB-012

`SI se evalúa G5 y la rama de trabajo figura en las ramas locales o en las referencias remotas de seguimiento, ENTONCES el validador DEBE registrar un error y NO DEBE declarar G5 superada.`

### CB-013

`SI el tag del release existe como objeto ligero o su mensaje no es `Release vX.Y.Z`, ENTONCES el validador DEBE registrar un error y NO DEBE declarar G6 superada.`

### CB-014

`SI una spec de `SPEC-001` a `SPEC-009` incumple una comprobación incorporada con posterioridad a su publicación, ENTONCES el validador DEBE registrar una advertencia de legado y NO DEBE devolver código de salida 1 por ese motivo.`

### CB-015

`SI el commit que introdujo la línea de aprobación es un commit de merge, ENTONCES el validador DEBE inspeccionar el commit no merge que introdujo la línea y DEBE verificar la firma de ese commit.`

## Fuera de alcance

- Los permisos de agentes, la materialización del rol de auditoría en `.opencode/` y la integración continua: corresponden al bloque B3 del informe de auditoría.
- El enlace `CA → T`, la evidencia por tarea y el vínculo entre commit, merge y release: corresponden al bloque B4 del informe de auditoría.
- La modificación de `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md` y las plantillas: la base v2 se cierra en el bloque B1.
- La alineación de la plantilla de rango 5 con la subsección `### Historial de transiciones`: si la plantilla debiera declararla, la alineación corresponde a una spec de la base y se registra como dependencia.
- La verificación remota directa de G5: la comprobación se limita a las ramas locales y a las referencias remotas de seguimiento, y la consulta al remoto queda como comprobación no verificada.
- La reescritura de las specs publicadas `SPEC-001` a `SPEC-009`.
- Los parámetros de hardware, las cuantizaciones y los benchmarks de modelos.

## Criterios de aceptación

### CA-001

`DADO una spec en `tasked` con la verificación G2 registrada, CUANDO se invoca el comando `/sdd-implement`, ENTONCES la etapa se abre en la primera tarea; y DADA la misma spec sin la verificación G2 registrada, ENTONCES el comando se detiene sin escribir estado.`

Cubre: `RF-001`, `CB-009`.

### CA-002

`DADO una spec en `tasked`, CUANDO el comando inicia la primera tarea, ENTONCES `spec.md` declara `implementing` y una fila nueva de la transición T4 en la subsección `### Historial de transiciones`; y CUANDO se cierra la última tarea con evidencia transcrita y pruebas en verde, ENTONCES declara `implemented` y la fila de la transición T5.`

Cubre: `RF-002`, `RF-003`, `RF-016`.

### CA-003

`DADO el cierre de la etapa Implement, CUANDO se evalúa G3, ENTONCES la evaluación ocurre una sola vez sobre el conjunto de tareas, una tarea sin cerrar produce error y ninguna otra etapa evalúa G3.`

Cubre: `RF-004`.

### CA-004

`DADO una spec en `implemented` sin `validation_report.md`, CUANDO el rol `reviewer` ejecuta el comando `/sdd-validate`, ENTONCES escribe el reporte y no evalúa G4 ni escribe el estado `validated`; y la evaluación de G4 espera a que el reporte exista y a la firma del propietario en `spec.md`.`

Cubre: `RF-005`.

### CA-005

`DADO un reporte de validación escrito, CUANDO el propietario firma la aprobación de G4, ENTONCES el orquestador escribe `validated` con la fila de la transición T6 si el dictamen es `CONVERGIDO`; y con dictamen `NO CONVERGIDO` la spec permanece en `implemented`.`

Cubre: `RF-021`, `CB-010`.

### CA-006

`DADO `spec.md` y `validation_report.md` de una spec, CUANDO se busca el registro de G4, ENTONCES aparece solo en la sección de aprobaciones de `spec.md`, y una casilla de aprobación en el reporte produce error.`

Cubre: `RF-006`, `RF-020`, `CB-002`, `CB-003`.

### CA-007

`DADO `spec.md` con la casilla de G1 marcada, CUANDO se evalúa G1, ENTONCES el validador localiza el commit que introdujo la línea con `git log -S`, verifica su firma con `git verify-commit` y coteja la clave firmante con `docs/sdd/firmantes_autorizados`; sin firma que verifique la compuerta no se declara aprobada, y si el commit es de merge el validador inspecciona el commit no merge.`

Cubre: `RF-007`, `RF-010`, `CB-001`, `CB-015`.

### CA-008

`DADO un reporte con dictamen `CONVERGIDO` y cada fila de la matriz en `PASADO`, CUANDO se evalúa G4 sin la casilla de aprobación marcada en `spec.md`, ENTONCES la compuerta no se declara superada.`

Cubre: `RF-008`.

### CA-009

`DADO un release preparado, CUANDO se evalúa G6, ENTONCES la compuerta exige la aprobación en la entrada de `CHANGELOG.md`, el tag anotado con su mensaje y su commit objetivo, la coincidencia de `specs/INDEX.md` y `CHANGELOG.md` con el estado `released`, y la referencia al informe de auditoría de conformidad solo cuando el componente MINOR del tag supere al del tag anterior en orden SemVer.`

Cubre: `RF-009`, `RF-014`, `CB-007`, `CB-013`.

### CA-010

`DADO un `RF` o un `CB` de `spec.md` sin mención en una línea `Cubre:`, CUANDO se evalúa G2, ENTONCES el validador devuelve código de salida 1 con el identificador del requisito.`

Cubre: `RF-011`.

### CA-011

`DADA una spec en `implemented` con una tarea sin la casilla `Completada` marcada, CUANDO se ejecuta la validación agregada, ENTONCES el validador devuelve código de salida 1 con el identificador de la tarea.`

Cubre: `RF-012`, `CB-008`.

### CA-012

`DADO un release integrado, CUANDO se evalúa G5, ENTONCES la compuerta se declara superada solo con la integración de dos padres, la ejecución posterior del validador sin hallazgos y la ausencia de la rama de trabajo en las ramas locales y en las referencias remotas de seguimiento, sin consulta de red; y con la rama presente la compuerta falla.`

Cubre: `RF-013`, `CB-012`.

### CA-013

`DADO `spec.md` con un estado escrito que no es destino de una transición admitida desde la última fila de la subsección `### Historial de transiciones`, CUANDO se ejecuta el validador, ENTONCES devuelve código de salida 1 y no admite el estado; y con una compuerta evaluada desde un estado de origen distinto al exigido, ENTONCES registra error.`

Cubre: `RF-015`, `CB-004`.

### CA-014

`DADO un cambio de estado, CUANDO se consulta `spec.md`, ENTONCES la subsección `### Historial de transiciones` de `## Historial de cambios` contiene la fila con fecha, transición, origen, destino, responsable y evidencia; y sin fila el validador registra error.`

Cubre: `RF-016`, `CB-011`.

### CA-015

`DADO dos specs con relación de sucesión, CUANDO se ejecuta el validador, ENTONCES los campos `supersedes` y `superseded_by` son recíprocos, la spec sustituida figura en `superseded`, y una referencia sin carpeta o una asimetría producen error.`

Cubre: `RF-017`, `CB-005`, `CB-006`.

### CA-016

`DADO el validador, CUANDO completa una ejecución, ENTONCES imprime la lista de comprobaciones ejecutadas y la lista de comprobaciones no verificadas, y no presenta el resultado favorable como conformidad del régimen.`

Cubre: `RF-018`, `RNF-004`.

### CA-017

`DADA una comprobación nueva del validador, CUANDO se revisa la suite, ENTONCES existe una prueba positiva y una prueba negativa que la ejercitan.`

Cubre: `RF-019`.

### CA-018

`DADO el corpus vigente, CUANDO se ejecuta el validador dos veces consecutivas, ENTONCES devuelve el mismo veredicto y el mismo código de salida, completa en 60 segundos o menos y no realiza acceso a red.`

Cubre: `RNF-001`, `RNF-002`, `RNF-003`.

### CA-019

`DADO el repositorio antes y después de una ejecución del validador, CUANDO se comparan los archivos, ENTONCES no existe diferencia atribuible a la ejecución.`

Cubre: `RNF-005`.

### CA-020

`DADA una spec de `SPEC-001` a `SPEC-009`, CUANDO incumple una comprobación incorporada con posterioridad a su publicación, ENTONCES el validador registra la advertencia de legado y no devuelve código de salida 1 por ese motivo.`

Cubre: `CB-014`, `RNF-006`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación: ocho ambigüedades resueltas, historial de transiciones como subsección de `Historial de cambios`, separación entre `reviewer` y orquestador, localización del commit por firma, alcance local de G5, detección del release menor, ventana de legado hasta `SPEC-009` y formato exacto de aprobación |
| 0.3.0 | 2026-11-14 | Plan: arquitectura del validador y de los comandos, trece comprobaciones nuevas, once decisiones técnicas, estrategia TDD y matriz de cobertura de veintiún requisitos, seis no funcionales y quince casos borde |
| 0.4.0 | 2026-11-14 | Tareas: quince tareas atómicas con dependencias acíclicas, treinta y nueve pruebas nuevas, dos escritores declarados por allowlist y traspaso al `reviewer` |
| 0.5.0 | 2026-11-14 | Mecanismo implementado con trece comprobaciones y noventa y cuatro pruebas; revisión independiente con cinco brechas cerradas y dictamen `CONVERGIDO` 42/42; G4 aprobada y estado `validated` |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con `AMB-001` a `AMB-008` resueltos y los parches marcados |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | línea de G1 firmada en `spec.md` en el commit `f38eb6a` y `plan.md` escrito con sus decisiones |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` con los ocho campos, dependencias acíclicas y cobertura completa de requisitos y casos borde |
| 2026-11-14 | T4 | `tasked` | `implementing` | orquestador | G2 verificada y ejecución agrupada autorizada; quince tareas cerradas con evidencia y 86 pruebas en verde |
| 2026-11-14 | T5 | `implementing` | `implemented` | orquestador | G3 con `OK: sin hallazgos`, quince tareas cerradas y 86 pruebas en verde |
| 2026-11-14 | T6 | `implemented` | `validated` | `reviewer` y G4 | `validation_report.md` con dictamen `CONVERGIDO` 42/42 y línea de G4 firmada en `spec.md` |
