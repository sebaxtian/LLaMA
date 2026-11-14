---
id: SPEC-012
title: Trazabilidad profunda SDD verificable
status: implemented
version: 0.6.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/trazabilidad-profunda-sdd
release: ""
supersedes: ""
superseded_by: ""
---

# Trazabilidad profunda SDD verificable

## Contexto y objetivo

El informe `docs/sdd/auditoria_cumplimiento_sdd.md` concentra en el bloque B4 los defectos de la trazabilidad profunda. El protocolo exige la cadena `RF/CB → CA → T → evidencia`, y la práctica la corta en cuatro puntos. El contrato de tarea no portaba el criterio de aceptación hasta la base v2, y las tareas publicadas siguen sin declararlo, de modo que una tarea conforme a su contrato no permite reconstruir qué criterio satisface (`AUD-022`). En `SPEC-001`, `SPEC-004` y `SPEC-006` las tareas no mencionan criterio alguno y el enlace `CA → T` solo se reconstruye por tránsito a través del requisito (`AUD-041`). La evidencia por tarea no tiene formato declarado ni comprobación, por lo que el eslabón `T → evidencia` queda al criterio de quien redacta (`AUD-042`), y una tarea puede marcarse completada sin evidencia registrada (`AUD-072`). El vínculo entre la implementación y su commit produce una advertencia que no bloquea la integración, y la ejecución agregada omite las comprobaciones de historial (`AUD-043`). Ningún artefacto declara el merge que integra cada spec ni el tag de su release, aunque ambos constan en el historial (`AUD-044`).

Objetivo: fijar el contrato de la trazabilidad profunda que cierra los seis hallazgos del bloque B4, de modo que cada tarea declare el criterio de aceptación que satisface, cada tarea cerrada transcriba la evidencia que la acredita, la verificación agregada trate como error el commit de implementación sin referencia a su spec, y cada spec validada o publicada declare el commit de integración y el tag de release que la cierran.

Resultado esperado: criterio de aceptación obligatorio en cada tarea con correspondencia recíproca entre criterio y tarea; evidencia obligatoria de 20 caracteres o más y sin marca de pendiente en cada tarea completada; verificación de historial dentro de la ejecución agregada, con alcance declarado y con el commit sin referencia como error; declaración del commit de integración y del tag de release en la sección de cierre de integración del reporte de validación, con error cuando falte en una spec validada o publicada; regularización de `SPEC-001` a `SPEC-007` con esos campos añadidos, incremento de la posición PATCH y sin reescritura de su contenido funcional; y una comprobación por cada hallazgo con al menos una prueba positiva y una negativa.

La feature se redacta con la base v2 vigente. No modifica `docs/constitution.md`, `AGENTS.md`, el protocolo operativo, el flujo Git ni las plantillas de rango 5, y no reabre los bloques B1, B2 y B3 del informe. La regularización de las siete specs publicadas añade los campos de trazabilidad y no reescribe su contenido funcional: un requisito que exigiera cambio se tramita por una spec nueva y no por edición directa. La sección de cierre de integración que esta spec exige en el reporte se alinea con la plantilla de rango 5 mediante una spec de base, registrada como dependencia. Un resultado favorable del validador acredita la presencia y la coherencia de los eslabones declarados, no la veracidad de la evidencia transcrita ni la firma de un commit de aprobación.

### Trazabilidad con el informe de auditoría

| Hallazgo | Requisitos que lo resuelven | Criterios de aceptación |
|---|---|---|
| `AUD-022` | `RF-001` | `CA-001` |
| `AUD-041` | `RF-001`, `RF-002` | `CA-001`, `CA-003` |
| `AUD-042` | `RF-004`, `RNF-008` | `CA-004`, `CA-017` |
| `AUD-043` | `RF-005` | `CA-005`, `CA-006` |
| `AUD-044` | `RF-006` | `CA-007`, `CA-008` |
| `AUD-072` | `RF-004` | `CA-004` |

`RF-003`, `RF-007`, `RF-008` y `RF-009` no responden a un hallazgo: completan la correspondencia recíproca entre criterio y tarea, fijan la regularización de las specs publicadas y conservan la exención del historial histórico. Se verifican en `CA-002`, `CA-009` a `CA-012`.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`; no delega la firma y no acepta una aprobación emitida por un agente.
- **Orquestador (`sdd`):** ejecuta el validador y la suite, verifica G2, G3 y G5, escribe las transiciones `implementing`, `implemented` y `validated`, y registra el commit de integración y el tag de release en el reporte de la spec publicada; no declara aprobaciones.
- **Agente `planner`:** redacta `spec.md`, `clarify.md`, `plan.md` y `tasks.md` dentro de `specs/`, incluida la regularización de las tareas de las siete specs publicadas; no escribe reportes de validación ni la sección de aprobaciones.
- **Agente `coder`:** escribe en `src/`, `tests/` y `tools/` y cierra tareas en `tasks.md` con la evidencia transcrita; no escribe fuera de esas raíces.
- **Agente `reviewer`:** escribe el reporte de validación de la spec en curso, con la matriz de trazabilidad y la declaración del commit validado; no modifica código ni configuración y no declara G4.
- **Agente `auditor`:** lee la base normativa y las specs y registra los hallazgos de trazabilidad en su informe; no edita requisitos ni declara compuertas.

## Requisitos funcionales (EARS)

### RF-001

`El sistema DEBE declarar en el criterio de aceptación de cada tarea al menos un identificador `CA-NNN` de la spec a la que pertenece la tarea, y DEBE enumerar varios identificadores separados por coma.`

### RF-002

`SI una tarea declara en su criterio de aceptación un identificador `CA-NNN` que no existe en `spec.md`, o un identificador que pertenece a otra spec, ENTONCES el sistema DEBE registrar un error con el identificador de la tarea y el identificador del criterio.`

### RF-003

`SI un `CA-NNN` de `spec.md` no figura en el criterio de aceptación de ninguna tarea, ENTONCES el sistema DEBE registrar un error con el identificador del criterio.`

### RF-004

`El sistema DEBE exigir que cada tarea marcada como completada declare en el campo `Evidencia` una transcripción no vacía de la salida que la acredita, y DEBE registrar un error cuando el campo falte, conserve el marcador de la plantilla sin sustituir, contenga menos de 20 caracteres tras eliminar los espacios en blanco o coincida con la marca `pendiente`, con la marca `N/A` o con un término vetado por el protocolo.`

### RF-005

`CUANDO se ejecuta la validación agregada del corpus, el sistema DEBE ejecutar además las comprobaciones de historial sobre los commits posteriores al punto de integración de la rama actual o, en su defecto, sobre los últimos 50 commits, y DEBE registrar un error por cada commit de implementación que no declare la cadena `Spec: SPEC-NNN` con el identificador de la spec a la que sirve.`

### RF-006

`El sistema DEBE exigir que el reporte de validación declare una sección de cierre de integración con el identificador del commit de integración y el tag de release de la spec, DEBE registrar un error cuando una spec en estado `validated` no declare el commit de integración, y DEBE registrar un error cuando una spec en estado `released` no declare el tag de release.`

### RF-007

`CUANDO se implementa esta spec, el sistema DEBE regularizar las specs `SPEC-001` a `SPEC-007` añadiendo el criterio de aceptación y la evidencia a cada tarea, el campo de evidencia donde el contrato anterior no lo declaraba, y la sección de cierre de integración con el commit y el tag que constan en el historial y en el informe de auditoría, DEBE incrementar la posición PATCH de cada spec con una fila de motivo en su historial de cambios, y NO DEBE alterar requisito, caso borde, criterio, tarea, estimación ni estado.`

### RF-008

`El sistema DEBE conservar la exención del historial de transiciones de las specs cuya redacción es anterior a la base v2 y NO DEBE añadir filas de transición a un historial que no las declara.`

### RF-009

`El validador DEBE conservar la degradación a advertencia para las comprobaciones de una spec cuya regularización queda fuera del alcance declarado, DEBE registrar esa exención como cláusula de legado que no se amplía sin una spec posterior y NO DEBE aplicar la degradación a `SPEC-012` ni a las specs posteriores.`

## Requisitos no funcionales

### RNF-001

`La validación agregada del corpus DEBE completar en 300 segundos o menos sobre el commit validado.`

### RNF-002

`El validador NO DEBE requerir acceso a red, servicio externo ni credencial alguna para ejecutar las comprobaciones de trazabilidad.`

### RNF-003

`El validador DEBE conservar sus tres códigos de salida: 0 sin hallazgos, 1 con al menos un error de validación y 2 ante un error de uso del comando.`

### RNF-004

`La regularización DEBE conservar sin cambios el 100 % de los requisitos funcionales, los requisitos no funcionales y los criterios de aceptación de las specs `SPEC-001` a `SPEC-007`.`

### RNF-005

`Cada comprobación nueva DEBE declarar al menos una prueba positiva y una prueba negativa en la suite de pruebas del mecanismo de control.`

### RNF-006

`La degradación a advertencia DEBE alcanzar a 4 specs como máximo y DEBE limitarse a `SPEC-008`, `SPEC-009`, `SPEC-010` y `SPEC-011`.`

### RNF-007

`Dos ejecuciones del validador sobre el mismo commit DEBEN producir el mismo conjunto de hallazgos, con 0 diferencias entre ambas salidas.`

### RNF-008

`El campo `Evidencia` de una tarea completada DEBE contener 20 caracteres o más de texto transcrito tras eliminar los espacios en blanco, y NO DEBE consistir en una marca de pendiente.`

## Casos borde

### CB-001

`SI una tarea declara un `CA-NNN` que no existe en `spec.md`, ENTONCES la validación DEBE registrar un error y la tarea DEBE conservar su casilla de completada sin efecto sobre el resultado.`

### CB-002

`SI un `CA-NNN` queda sin tarea que lo declare, ENTONCES la validación DEBE registrar un error con el identificador del criterio y la spec DEBE permanecer en su estado con la brecha declarada.`

### CB-003

`SI una tarea declara un `CA-NNN` que pertenece a otra spec, ENTONCES la validación DEBE registrar un error por referencia cruzada y DEBE informar el identificador de la spec de destino.`

### CB-004

`SI una tarea está marcada como completada y su campo `Evidencia` conserva el marcador de la plantilla sin sustituir, contiene menos de 20 caracteres tras eliminar los espacios en blanco o coincide con la marca `pendiente`, con la marca `N/A` o con un término vetado por el protocolo, ENTONCES la validación DEBE registrar un error con el identificador de la tarea.`

### CB-005

`SI un commit de implementación no declara la cadena `Spec: SPEC-NNN`, ENTONCES la ejecución agregada DEBE registrar un error con el identificador del commit y DEBE devolver el código de salida 1.`

### CB-006

`SI el historial de la rama no contiene un commit de implementación sobre el que aplicar la comprobación, ENTONCES la ejecución agregada DEBE informar la comprobación como no aplicable y NO DEBE producir error por esa causa.`

### CB-007

`SI una spec en estado `validated` no declara el commit de integración en su reporte de validación, ENTONCES la validación DEBE registrar un error con el identificador de la spec.`

### CB-008

`SI una spec en estado `released` no declara el tag de release en su reporte de validación, ENTONCES la validación DEBE registrar un error con el identificador de la spec.`

### CB-009

`SI el tag declarado en el reporte difiere del campo `release` del frontmatter o de la fila de la spec en el índice del corpus, ENTONCES la validación DEBE registrar un error con los dos valores en conflicto.`

### CB-010

`SI una spec fuera del alcance declarado incurre en una de las faltas de trazabilidad de esta spec, ENTONCES la validación DEBE registrar una advertencia y NO DEBE devolver error por esa causa; la exención NO DEBE alcanzar a `SPEC-012` ni a las specs posteriores.`

### CB-011

`SI la regularización de una spec publicada exige cambiar un requisito, un requisito no funcional o un criterio de aceptación, ENTONCES la regularización DEBE detenerse para esa spec, el cambio DEBE tramitarse como incremento MINOR en una spec nueva y la necesidad DEBE registrarse como dependencia.`

### CB-012

`SI el reporte de una spec publicada declara un dictamen no convergido, ENTONCES el registro del commit de integración y del tag de release DEBE añadirse sin alterar la matriz ni el dictamen, y la brecha DEBE conservarse con su motivo.`

### CB-013

`SI una tarea publicada carece del campo `Evidencia` porque su contrato anterior no lo declaraba, ENTONCES la regularización DEBE añadir el campo con la evidencia de la tarea y NO DEBE alterar el texto de las dependencias, los requisitos cubiertos, los archivos ni la estimación.`

### CB-014

`SI el historial de transiciones de una spec publicada no declara la subsección, ENTONCES la validación DEBE registrar una advertencia y NO DEBE registrar un error, y la regularización NO DEBE añadir fila de transición alguna.`

### CB-015

`SI una tarea declara varios identificadores de criterio de aceptación sin separarlos por coma, ENTONCES la validación DEBE registrar un error de formato con el identificador de la tarea.`

### CB-016

`SI una spec en estado `validated` o `released` no declara la sección de cierre de integración, ENTONCES la validación DEBE registrar un error con el identificador de la spec.`

### CB-017

`SI una spec regularizada no incrementa la posición PATCH de su versión o no registra la fila de motivo en su historial de cambios, ENTONCES la validación DEBE registrar un error de versionado con el identificador de la spec.`

### CB-018

`SI un commit de implementación anterior al punto de integración de la rama no declara la cadena `Spec: SPEC-NNN`, ENTONCES la comprobación DEBE quedar cubierta por la ventana de legado y NO DEBE producir error.`

## Fuera de alcance

- El cambio de regla en `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md` y las plantillas de rango 5: la base v2 fija la regla de la cadena y esta spec la verifica; una necesidad de cambio de regla se registra como dependencia y exige una spec de base.
- Los bloques B1, B2 y B3 del informe de auditoría: el mecanismo de control y la práctica operativa quedaron cerrados en `SPEC-009`, `SPEC-010` y `SPEC-011`.
- La reescritura del contenido funcional de las specs publicadas `SPEC-001` a `SPEC-007`: la regularización añade los campos de trazabilidad y no modifica requisitos, criterios ni comportamiento declarado.
- La alteración de `SPEC-008`, `SPEC-009`, `SPEC-010` y `SPEC-011`: su regularización queda fuera del alcance declarado y conserva la degradación a advertencia.
- La ampliación de la ventana de legado: la exención de `SPEC-008` a `SPEC-011` queda registrada como cláusula de legado y su ampliación exige una spec posterior.
- La alineación de la plantilla de rango 5 del reporte de validación con la sección de cierre de integración: se registra como dependencia de una spec de base; esta spec exige la sección, su contenido y su comprobación.
- La verificación de la veracidad de la evidencia transcrita en una tarea: el validador comprueba la presencia y la forma del registro y no su correspondencia con una ejecución real.
- La instalación de un hook local de historial: la comprobación del commit se ejecuta dentro de la validación agregada.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.
- Los modelos, las cuantizaciones, el hardware y los benchmarks de ejecución local.

## Criterios de aceptación

### CA-001

`DADAS las tareas de una spec, CUANDO se ejecuta la validación, ENTONCES cada tarea declara al menos un identificador `CA-NNN` en su criterio de aceptación, los identificadores múltiples se enumeran separados por coma, y una tarea cuyo criterio declare un identificador inexistente o mal separado produce un error con el identificador de la tarea y el del criterio.`

Cubre: `RF-001`, `RF-002`, `CB-001`, `CB-015`.

### CA-002

`DADOS los criterios de aceptación de una spec y sus tareas, CUANDO se ejecuta la validación, ENTONCES el criterio declarado por al menos una tarea no produce hallazgo y el criterio que ninguna tarea declara produce un error con su identificador.`

Cubre: `RF-003`, `CB-002`.

### CA-003

`DADA una tarea que declara un identificador de criterio perteneciente a otra spec, CUANDO se ejecuta la validación, ENTONCES se registra un error por referencia cruzada con el identificador de la spec de destino.`

Cubre: `RF-002`, `CB-003`.

### CA-004

`DADA una tarea marcada como completada, CUANDO su campo de evidencia falta, conserva el marcador de la plantilla, contiene menos de 20 caracteres tras eliminar los espacios en blanco o coincide con una marca de pendiente, ENTONCES se registra un error con el identificador de la tarea; y una tarea no completada sin evidencia no produce error.`

Cubre: `RF-004`, `RNF-008`, `CB-004`.

### CA-005

`DADO un corpus con commits de implementación posteriores al punto de integración de la rama, CUANDO se ejecuta la validación agregada, ENTONCES ejecuta las comprobaciones de historial y un commit sin la cadena `Spec: SPEC-NNN` produce un error con el identificador del commit y el código de salida 1.`

Cubre: `RF-005`, `CB-005`.

### CA-006

`DADO un historial sin commit de implementación posterior al punto de integración, o con commits anteriores a ese punto, CUANDO se ejecuta la validación agregada, ENTONCES la comprobación se informa como no aplicable o cubierta por la ventana de legado y el código de salida es 0 cuando no existe otro hallazgo.`

Cubre: `RF-005`, `CB-006`, `CB-018`.

### CA-007

`DADA una spec en estado `validated` o `released`, CUANDO su reporte de validación no declara la sección de cierre de integración, o no declara el commit de integración o el tag de release según su estado, ENTONCES se registra un error con el identificador de la spec; y el reporte que declara la sección con ambos valores no produce hallazgo por esa causa.`

Cubre: `RF-006`, `CB-007`, `CB-008`, `CB-016`.

### CA-008

`DADO un tag declarado en el reporte, CUANDO difiere del campo `release` del frontmatter o de la fila de la spec en el índice del corpus, ENTONCES se registra un error con los dos valores en conflicto.`

Cubre: `RF-006`, `CB-009`.

### CA-009

`DADAS las specs `SPEC-001` a `SPEC-007` regularizadas, CUANDO se ejecuta la validación agregada, ENTONCES cada tarea declara al menos un criterio de aceptación y una evidencia, cada reporte declara la sección de cierre de integración con su commit y su tag, y no se registra error de trazabilidad por esas siete specs.`

Cubre: `RF-007`, `CB-013`.

### CA-010

`DADAS las specs `SPEC-001` a `SPEC-007` regularizadas, CUANDO se contrasta cada artefacto con su versión anterior, ENTONCES el 100 % de sus requisitos funcionales, requisitos no funcionales, casos borde, criterios y estimaciones queda sin cambios, el historial de cambios registra la fila de la regularización con el motivo y el incremento de la posición PATCH, y la falta de ese incremento o de esa fila produce un error de versionado.`

Cubre: `RF-007`, `RNF-004`, `CB-017`.

### CA-011

`DADA una spec publicada con historial de transiciones, CUANDO se regulariza, ENTONCES su historial de transiciones conserva sus filas sin edición y sin filas nuevas, su estado vigente no cambia, y un historial histórico sin la subsección produce una advertencia y no un error.`

Cubre: `RF-008`, `CB-014`.

### CA-012

`DADAS las specs fuera del alcance declarado, CUANDO incurren en una falta de trazabilidad, ENTONCES la validación registra una advertencia y no devuelve error; y la misma falta en `SPEC-012` o en una spec posterior produce un error.`

Cubre: `RF-009`, `RNF-006`, `CB-010`.

### CA-013

`DADA una spec publicada cuya regularización exige cambiar un requisito, un requisito no funcional o un criterio de aceptación, CUANDO se detecta la necesidad, ENTONCES la regularización se detiene para esa spec y la necesidad queda registrada como dependencia de una spec nueva.`

Cubre: `CB-011`.

### CA-014

`DADO un reporte de validación con dictamen no convergido y brecha consignada, CUANDO se registra el commit de integración y el tag de release, ENTONCES la matriz y el dictamen quedan sin alteración y la brecha conserva su motivo.`

Cubre: `CB-012`.

### CA-015

`DADO el corpus en el commit validado, CUANDO se ejecuta la validación agregada en dos ocasiones, ENTONCES completa en 300 segundos o menos en cada ejecución y las dos salidas presentan 0 diferencias en el conjunto de hallazgos.`

Cubre: `RNF-001`, `RNF-007`.

### CA-016

`DADO un entorno sin acceso a red, CUANDO se ejecuta la validación de trazabilidad, ENTONCES completa sin requerir red, servicio externo ni credencial, y conserva los códigos de salida 0 sin hallazgos, 1 con error de validación y 2 ante error de uso.`

Cubre: `RNF-002`, `RNF-003`.

### CA-017

`DADAS las comprobaciones nuevas de trazabilidad, CUANDO se inspecciona la suite de pruebas, ENTONCES cada una declara al menos una prueba positiva y una prueba negativa y el caso negativo produce el código de salida 1.`

Cubre: `RNF-005`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación: ocho ambigüedades resueltas; umbral y marcas de pendiente de la evidencia; ventana de legado de cuatro specs; versionado PATCH de la regularización; fuente histórica de merge y tag; sección de cierre de integración; alcance de la comprobación de commits; separación por coma de varios criterios; regularización sin reescritura; cuatro casos borde nuevos |
| 0.3.0 | 2026-11-14 | Plan: arquitectura de seis capas, procedimientos de las cinco comprobaciones nuevas, contratos de tarea, evidencia, cierre de integración y regularización con la tabla de siete pares, diez decisiones técnicas y matriz de cobertura de nueve requisitos, ocho no funcionales y dieciocho casos borde |
| 0.4.0 | 2026-11-14 | Tareas: dieciocho tareas atómicas con dependencias acíclicas, tres escritores declarados, veinte pruebas nuevas en cinco tareas de prueba y cobertura completa de requisitos y casos borde |
| 0.5.0 | 2026-11-14 | Implementación de la trazabilidad profunda |
| 0.6.0 | 2026-11-14 | Cierre de la implementación y verificación G3 |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con nueve requisitos funcionales, ocho no funcionales, catorce casos borde y diecisiete criterios de aceptación |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con `AMB-001` a `AMB-008` resueltos, cuatro casos borde nuevos y once parches marcados en `spec.md` |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | línea de G1 firmada en `spec.md` en el commit `cfb576b` y `plan.md` escrito con diez decisiones y la matriz de cobertura de treinta y cinco filas |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` con dieciocho tareas, ocho campos por tarea, dependencias acíclicas y cobertura de nueve requisitos, ocho no funcionales y dieciocho casos borde |
| 2026-11-14 | T4 | `tasked` | `implementing` | `planner` | dieciocho tareas cerradas con criterio de aceptación y evidencia, ventana de legado limitada a `SPEC-008` a `SPEC-011` y `--all` con código 0 |
| 2026-11-14 | T5 | `implementing` | `implemented` | `planner` | G3 verificada en el commit `a3a2794` con dieciocho tareas cerradas, 131 pruebas en verde y `--all` con código 0 |
