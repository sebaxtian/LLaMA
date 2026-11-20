---
id: SPEC-015
title: Cierre de la auditoría posterior al release
status: released
version: 0.8.0
created: 2026-11-20
updated: 2026-11-21
owner: Agent Sebaxtian
branch: feat/cierre-auditoria-posterior
release: "v0.7.1"
supersedes: ""
superseded_by: ""
---

# Cierre de la auditoría posterior al release

## Contexto y objetivo

La auditoría de conformidad registrada en `docs/sdd/auditoria_posterior_v0_7_0.md` evaluó la base normativa v2, las catorce specs, el validador, las dos suites, la matriz de agentes, el flujo de integración continua y el historial Git sobre el commit `13e85e2`, y emitió el veredicto global `NO CONFORME` con 10 observaciones vigentes: 3 de severidad Alta, 4 de severidad Media y 3 de severidad Baja. Las tres observaciones de severidad Alta se concentran en el proceso de release del estado publicado: el tag `v0.7.0` se recreó para incorporar la cita de auditoría que la condición del incremento MINOR exige, el commit de empaquetado modificó 18 archivos en lugar de los 3 previstos y la entrada protegida del release recibió una modificación sin firma.

Las siete observaciones restantes son de sección documental, de fila de validación o de registro. `AUD-099` quedó cerrada mediante la fila del informe de auditoría en la tabla de inventario de `docs/sdd/README.md`. Las seis restantes esperan la corrección declarada: la nota de cierre del reporte de `SPEC-013` debe resolver la evidencia diferida de `RNF-001` y de `CA-015`; el reporte de `SPEC-014` debe registrar el resultado de G6; la fila T7 de `SPEC-014` debe declarar el release publicado en lugar del tag pendiente; y las tres correcciones de alineación del rango 4, del §12 del protocolo y del registro de cambios deben quedar aplicadas.

Objetivo: fijar el contrato que cierra las 10 observaciones del informe posterior, de modo que cada una quede cerrada con el artefacto que la satisface y con evidencia verificable, y que el release `v0.7.1` se publique por el procedimiento vigente con el tag `v0.7.0` sin movimiento.

Resultado esperado: procedimiento escrito de corrección de un tag publicado con 3 condiciones habilitantes y registro del identificador anterior; alcance de la rama de empaquetado limitado a 4 artefactos con exigencia de spec o de fix previo para cualquier otra ruta; exigencia de commit firmado para la modificación de una entrada publicada; nota append-only del resultado de G6 en el reporte de `SPEC-014`; nota de cierre corregida en el reporte de `SPEC-013` que declara el valor efectivo de las 2 filas diferidas y el cierre de las 7 observaciones del informe final; fila T7 de `SPEC-014` con el release publicado y su incremento PATCH; y las 3 correcciones de alineación aplicadas.

La feature no reescribe historia publicada, no mueve el tag `v0.7.0`, no cambia requisitos de las specs publicadas más allá de las correcciones declaradas y no reabre el contenido funcional de `SPEC-013` ni de `SPEC-014`. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen ni la autorización de un release.

### Trazabilidad con el informe de auditoría

| Observación | Severidad | Requisito | Criterio de aceptación |
|---|---|---|---|
| `AUD-087` | Alta | `RF-001` | `CA-001` |
| `AUD-088` | Alta | `RF-002` | `CA-002` |
| `AUD-090` | Alta | `RF-003` | `CA-003` |
| `AUD-089` | Media | `RF-004` | `CA-004` |
| `AUD-076` | Media | `RF-005` | `CA-005` |
| `AUD-057` | Media | `RF-006` | `CA-006` |
| `AUD-039` | Baja | `RF-007` | `CA-007` |
| `AUD-068` | Baja | `RF-008` | `CA-007` |
| `AUD-100` | Baja | `RF-009` | `CA-007` |
| `AUD-099` | Media | `RF-010` | `CA-008` |
| Las 10 observaciones | Alta, Media y Baja | `RF-010` | `CA-008` |
| Release `v0.7.1` | No aplica | `RF-011` | `CA-009` |

Cada una de las 10 observaciones queda cubierta por un requisito funcional y por al menos un criterio de aceptación. Los requisitos no funcionales y los casos borde completan las condiciones de cierre y no responden a una observación aislada.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`, emite la autorización escrita que habilita la corrección de un tag publicado, firma la modificación de cada entrada de release publicada y declara G6 en la entrada del release; no delega la firma.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de `specs/015-cierre-auditoria-posterior/`, escribe las transiciones T1 a T3 y escribe las transiciones T4 a T7 sobre la verificación registrada por el orquestador; no escribe fuera de `specs/`, no redacta reporte de validación y no declara compuertas.
- **Agente `coder`:** escribe en `tools/` las comprobaciones del procedimiento de corrección de tag, del alcance de la rama de empaquetado y de la firma posterior a la publicación, y cierra tareas en `tasks.md` con la evidencia transcrita.
- **Agente `documenter`:** redacta las correcciones de `docs/Flujo_de_Trabajo_Git.md`, de `docs/sdd/PROTOCOLO_OPERATIVO.md` y de `CHANGELOG.md` dentro del alcance declarado y como delegado explícito del propietario; no modifica la sección de aprobaciones de una spec.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec y, por delegación escrita del propietario, escribe las notas append-only en el reporte de `SPEC-013` y en el reporte de `SPEC-014`, sin alterar matriz ni dictamen; no declara G4.
- **Orquestador (`sdd`):** verifica G2, G3 y G5, registra el resultado de cada verificación, ejecuta el validador y `git add` y `git commit` de los artefactos de control; no redacta artefacto alguno y no declara aprobación.
- **Agente `auditor`:** ejecuta la auditoría de conformidad del release `v0.7.1`, registra el veredicto por dimensión y el estado de cada observación en el informe que produce; no edita requisitos y no declara compuertas.

## Requisitos funcionales (EARS)

### RF-001

`CUANDO una consecuencia de un release publicado exige corregir su etiqueta, el sistema DEBE exigir las 3 condiciones habilitantes de la tabla de este requisito de forma simultánea, DEBE registrar el identificador del tag anterior y el identificador del nuevo destino antes de ejecutar la corrección, DEBE ejecutar la corrección antes de que un consumidor dependa del tag, y NO DEBE mover, eliminar ni reutilizar un tag publicado sin las 3 condiciones.`

Condiciones habilitantes de la corrección de un tag publicado:

| Condición | Evidencia exigida | Efecto de su ausencia |
|---|---|---|
| Autorización escrita del propietario | registro escrito con la fecha y el alcance de la corrección | la corrección no se ejecuta |
| Registro del identificador anterior | identificador completo del tag anterior y del destino nuevo en el informe de cierre | la corrección no se registra y la observación permanece vigente |
| Ausencia de consumidores del tag | declaración del propietario de que ningún consumidor depende del tag | la corrección se tramita por un release PATCH nuevo |

Cierre del caso del release `v0.7.0`: se registra como excepción del procedimiento con el tag anterior `ad739a0` y el destino vigente `5a3af48`, queda declarada la deuda aceptada del release publicado y el tag no se mueve de nuevo.

### RF-002

`El sistema DEBE limitar la rama de empaquetado `release/vX-Y-Z` a la modificación de los 4 artefactos de la tabla de este requisito, DEBE exigir una spec previa o un fix previo para cualquier modificación de una ruta distinta de las 4 declaradas, DEBE declarar ese alcance en la norma de integración de rango 4, y NO DEBE admitir en esa rama la escritura de documentación operativa, de código, de pruebas ni de configuración del repositorio.`

Artefactos admitidos en la rama de empaquetado:

| Artefacto | Modificación admitida |
|---|---|
| `CHANGELOG.md` | entrada del release e historial de releases |
| `specs/INDEX.md` | fila de la spec publicada |
| Frontmatter de una spec publicada | campos `status`, `version`, `updated` y `release` |
| Línea `Release:` de un reporte de validación publicado | tag del release |

Cierre del caso del empaquetado de `v0.7.0`: el commit `5da6df6` modificó 18 archivos, entre ellos `MEMORY.md` y una suite de pruebas, y se registra como excepción del alcance con la regularización de la comprobación afectada por esta spec y con su fila en el registro de cambios.

### RF-003

`CUANDO se modifica una entrada publicada de `CHANGELOG.md` o un artefacto de una spec publicada, el sistema DEBE registrar la modificación en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, DEBE transcribir el estado de firma del commit en la evidencia del cierre, y NO DEBE admitir la modificación de una entrada publicada en un commit sin firma verificable.`

### RF-004

`El sistema DEBE añadir al reporte de validación de `SPEC-014` una nota append-only que transcriba el resultado de las 3 verificaciones de release —tag anotado verificado con su commit objetivo, `specs/INDEX.md` y `CHANGELOG.md` actualizados, y línea de G6 firmada—, DEBE conservar sin alteración la matriz de trazabilidad y el dictamen de esa spec, DEBE conservar su estado `released`, y NO DEBE declarar compuerta alguna.`

### RF-005

`El sistema DEBE corregir la nota de cierre del reporte de validación de `SPEC-013` mediante 1 nota posterior append-only que declare el valor efectivo de `RNF-001` y de `CA-015` que la evidencia sostiene, DEBE registrar en esa nota el cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y la séptima cerrada por esta spec, DEBE conservar las filas de la matriz de trazabilidad y el dictamen `CONVERGIDO`, y NO DEBE reescribir el criterio publicado ni declarar superado un criterio cuya evidencia no lo sostiene.`

### RF-006

`El sistema DEBE sustituir la evidencia de la fila T7 del historial de transiciones de `SPEC-014` por el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, DEBE incrementar la versión de `SPEC-014` en 1 incremento PATCH a 0.8.1 con 1 fila de motivo de regularización en su historial de cambios, DEBE conservar el destino `released` y el campo `release` de esa spec, y NO DEBE renumerar la spec ni reescribir sus requisitos ni sus criterios de aceptación.`

### RF-007

`El sistema DEBE incorporar el check `verify` a la condición de la fila G5 de la tabla de compuertas de `docs/Flujo_de_Trabajo_Git.md`, DEBE declararlo exigible con `strict: true` en `main` y en `dev`, DEBE conservar la regla de bloqueo que ese documento ya declara, y NO DEBE dejar la definición de la compuerta más estrecha que la regla del mismo documento.`

### RF-008

`El sistema DEBE retirar del bloque de documentos de raíz de §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` la remisión al bloque B3, DEBE sustituirla por la referencia a la matriz de permisos vigente y a su formalización ejecutada, y NO DEBE declarar pendiente una formalización ya presente en la matriz y en el propio §12.`

### RF-009

`El sistema DEBE corregir el párrafo posterior al historial de releases de `CHANGELOG.md` para declarar en tiempo pasado la línea de G6 registrada en la entrada del release y la creación del tag `v0.7.0`, DEBE enumerar en la viñeta de la entrada los 16 identificadores asignados que esa entrada cita en lugar del rango `AUD-038` a `AUD-102`, y NO DEBE conservar un rango que incluya un número no asignado.`

Identificadores asignados que la viñeta de la entrada del release cita: `AUD-038`, `AUD-057`, `AUD-066`, `AUD-067`, `AUD-068`, `AUD-075`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-098`, `AUD-099`, `AUD-100`, `AUD-101` y `AUD-102`.

### RF-010

`El sistema DEBE cerrar las 10 observaciones `AUD-039`, `AUD-057`, `AUD-068`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-099` y `AUD-100` con el artefacto que las satisface y con la evidencia transcrita por ruta y línea, DEBE registrar `AUD-099` como cerrada por la fila del informe en la tabla de inventario de `docs/sdd/README.md`, DEBE declarar 10 de 10 cerradas en el informe de la auditoría de `v0.7.1`, y NO DEBE declarar cerrada una observación que conserve causa vigente ni cerrarla sin evidencia.`

### RF-011

`El sistema DEBE publicar el release `v0.7.1` por el procedimiento de `docs/Flujo_de_Trabajo_Git.md` con la verificación de G5 registrada, con el tag anotado de mensaje `Release v0.7.1`, con la línea de G6 firmada en su entrada de `CHANGELOG.md`, con `specs/INDEX.md` y `CHANGELOG.md` actualizados y con el informe de la auditoría de conformidad registrado, DEBE conservar el tag `v0.7.0` sin movimiento, y NO DEBE publicar el release sin la verificación de G5 ni sin la auditoría de conformidad registrada.`

## Requisitos no funcionales

### RNF-001

`El número de filas de matriz de trazabilidad y de dictámenes de specs publicadas alterados por esta spec DEBE ser 0.`

### RNF-002

`El tag `v0.7.1` DEBE ser 1 objeto anotado con el mensaje `Release v0.7.1` y DEBE apuntar a 1 commit de `main` que sea ancestro de `dev`.`

### RNF-003

`La validación agregada DEBE completar en 300 segundos o menos sobre el commit validado.`

### RNF-004

`Las correcciones de esta spec DEBEN conservar el 100 % de los requisitos y de los criterios de aceptación de las specs publicadas que no sean objeto de una corrección declarada, y el número de requisitos renumerados DEBE ser 0.`

## Casos borde

### CB-001

`SI la corrección de un tag publicado carece de autorización escrita del propietario, ENTONCES el sistema NO DEBE mover ni recrear el tag y DEBE registrar la observación como deuda aceptada del release publicado.`

### CB-002

`SI un consumidor depende del tag publicado, ENTONCES el sistema NO DEBE ejecutar la corrección sobre ese tag y DEBE tramitarla por un release PATCH nuevo con su propio tag.`

### CB-003

`SI la rama de empaquetado modifica una ruta distinta de los 4 artefactos admitidos, ENTONCES la verificación DEBE registrar un error que nombre la ruta y NO DEBE declarar conforme el empaquetado.`

### CB-004

`SI la modificación posterior a la publicación no está firmada por una clave de `docs/sdd/firmantes_autorizados`, ENTONCES la verificación DEBE registrar el estado de firma del commit y NO DEBE declarar válida la modificación.`

### CB-005

`SI el reporte de `SPEC-014` ya declara una nota del resultado de G6, ENTONCES la nota nueva DEBE añadirse a continuación sin eliminar la anterior y sin alterar la matriz ni el dictamen.`

### CB-006

`SI la corrección de la fila T7 de `SPEC-014` altera el destino `released` o el identificador del release, ENTONCES la corrección DEBE rechazarse y el conflicto DEBE registrarse en el reporte de esa spec.`

### CB-007

`SI el release `v0.7.1` se intenta publicar con un tag existente, ENTONCES el procedimiento DEBE detenerse antes de crear el tag y DEBE registrar el identificador del tag en conflicto.`

### CB-008

`SI una de las 10 observaciones carece de artefacto de cierre, ENTONCES el informe de la auditoría de `v0.7.1` NO DEBE declararla cerrada y DEBE registrar su causa como vigente.`

## Fuera de alcance

- La recreación y el desplazamiento del tag `v0.7.0`: se conserva en su destino `5a3af48` y su corrección queda registrada como excepción.
- La reescritura de historia publicada, con rebase, squash o copia manual de commits integrados.
- El cambio de requisitos de specs publicadas más allá de las correcciones declaradas en `RF-005`, `RF-006`, `RF-007`, `RF-008` y `RF-009`.
- La reapertura del contenido funcional de `SPEC-013` y de `SPEC-014`: se añaden notas y se corrige 1 fila de transición.
- La modificación de `docs/sdd/auditoria_posterior_v0_7_0.md`: se cita como evidencia y no se modifica.
- La corrección de `AUD-099`: quedó cerrada con la fila del informe en la tabla de inventario.
- La ampliación del alcance del validador a la ejecución real del flujo en GitHub.
- El cambio de la configuración remota de protección de ramas por una vía distinta de las reglas declaradas.
- Hardware, modelos, cuantizaciones y benchmarks de ejecución local.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.

## Criterios de aceptación

### CA-001

`DADO el procedimiento de corrección de un tag publicado, CUANDO se contrasta con la norma de integración de rango 4 y con el caso del release `v0.7.0`, ENTONCES el procedimiento exige las 3 condiciones habilitantes de forma simultánea, registra el identificador del tag anterior y el del destino nuevo, se ejecuta antes de que un consumidor dependa del tag, la falta de autorización escrita impide mover o recrear el tag y deja la observación como deuda aceptada, la dependencia de un consumidor desplaza la corrección a un release PATCH nuevo, y el caso `v0.7.0` figura como excepción con el tag anterior `ad739a0` y el destino `5a3af48`.`

Cubre: `RF-001`, `CB-001`, `CB-002`.

### CA-002

`DADO el commit de empaquetado de un release, CUANDO se contrasta con el alcance declarado de la rama `release/vX-Y-Z` y con el commit `5da6df6`, ENTONCES el alcance admitido son los 4 artefactos declarados, cualquier ruta distinta exige una spec previa o un fix previo, la norma de integración de rango 4 declara ese alcance, una ruta fuera del alcance produce un error que la nombra, y el caso `v0.7.0` figura como excepción con la regularización de la comprobación afectada.`

Cubre: `RF-002`, `CB-003`.

### CA-003

`DADO un artefacto publicado de `CHANGELOG.md` o de una spec publicada, CUANDO se modifica, ENTONCES la modificación consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, el estado de firma se transcribe en la evidencia del cierre, y una modificación sin firma verificable produce el registro del estado de firma y no se declara válida.`

Cubre: `RF-003`, `CB-004`.

### CA-004

`DADO el reporte de validación de `SPEC-014`, CUANDO se añade la nota del resultado de G6, ENTONCES la nota figura a continuación de las notas precedentes y transcribe el tag anotado verificado con su commit objetivo, la actualización de `specs/INDEX.md` y de `CHANGELOG.md` y la línea de G6 firmada, la matriz de trazabilidad y el dictamen conservan su contenido, el estado `released` no cambia y la nota no declara compuerta alguna.`

Cubre: `RF-004`, `CB-005`.

### CA-005

`DADO el reporte de validación de `SPEC-013`, CUANDO se añade la nota de cierre corregida, ENTONCES la nota declara el valor efectivo de `RNF-001` y de `CA-015` que la evidencia sostiene, registra el cierre de las 7 observaciones del informe final con 6 cerradas con artefacto y la séptima cerrada por esta spec, las filas de la matriz y el dictamen `CONVERGIDO` conservan su contenido, y ningún criterio publicado se reescribe ni se declara superado sin evidencia que lo sostenga.`

Cubre: `RF-005`.

### CA-006

`DADAS la spec `SPEC-014` y la fila T7 de su historial de transiciones, CUANDO se corrige la evidencia y se incrementa la versión, ENTONCES la fila declara el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, la versión pasa a 0.8.1 con 1 fila de motivo de regularización, el destino `released` y el campo `release` se conservan, la spec no se renumera, y una corrección que altere el destino o el identificador del release se rechaza con el conflicto registrado.`

Cubre: `RF-006`, `CB-006`.

### CA-007

`DADOS `docs/Flujo_de_Trabajo_Git.md`, §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` y `CHANGELOG.md`, CUANDO se contrastan las 3 correcciones de alineación, ENTONCES la fila G5 del rango 4 incorpora el check `verify` exigible con `strict: true` en `main` y en `dev` sin alterar la regla de bloqueo, §12 referencia la matriz de permisos vigente sin remitir al bloque B3 ni declarar pendiente una formalización ejecutada, el párrafo posterior al historial de releases declara en tiempo pasado la línea de G6 y la creación del tag `v0.7.0`, y la viñeta de la entrada enumera los 16 identificadores asignados sin un rango que incluya números no asignados.`

Cubre: `RF-007`, `RF-008`, `RF-009`.

### CA-008

`DADAS las 10 observaciones del informe posterior, CUANDO se contrastan con su artefacto de cierre y con el informe de la auditoría de `v0.7.1`, ENTONCES las 10 cuentan con artefacto y evidencia transcrita por ruta y línea, `AUD-099` figura cerrada por la fila del informe en la tabla de inventario, el informe declara 10 de 10 cerradas, y una observación sin artefacto de cierre queda registrada como vigente y no se declara cerrada.`

Cubre: `RF-010`, `CB-008`.

### CA-009

`DADO el release `v0.7.1`, CUANDO se publica por el procedimiento de `docs/Flujo_de_Trabajo_Git.md`, ENTONCES la verificación de G5 figura registrada, el tag es 1 objeto anotado de mensaje `Release v0.7.1` que apunta a 1 commit de `main` ancestro de `dev`, la línea de G6 figura firmada en su entrada de `CHANGELOG.md`, `specs/INDEX.md` y `CHANGELOG.md` figuran actualizados, el informe de la auditoría figura registrado, el tag `v0.7.0` conserva su destino, y un tag existente detiene el procedimiento con el identificador en conflicto registrado.`

Cubre: `RF-011`, `CB-007`.

### CA-010

`DADO el corpus en el commit validado, CUANDO se ejecuta la validación agregada y se contrastan las specs publicadas con su versión anterior, ENTONCES la ejecución completa en 300 segundos o menos, el número de filas de matriz y de dictámenes alterados es 0, el 100 % de los requisitos y de los criterios de las specs publicadas que no son objeto de corrección declarada se conserva y el número de requisitos renumerados es 0.`

Cubre: `RNF-001`, `RNF-003`, `RNF-004`.

### CA-011

`DADO el tag `v0.7.1` creado, CUANDO se verifica su tipo, su mensaje y su commit objetivo, ENTONCES resuelve a 1 objeto anotado con el mensaje `Release v0.7.1`, apunta a 1 commit de `main` y ese commit es ancestro de `dev`.`

Cubre: `RNF-002`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-20)
- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-20)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-20 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-20 | Clarificación cerrada: 11 ambigüedades resueltas y parches aplicados a los requisitos funcionales, los requisitos no funcionales, los casos borde, los criterios de aceptación, los actores y el alcance |
| 0.3.0 | 2026-11-20 | Plan técnico cerrado: doce componentes, contratos `C-1` a `C-8`, decisiones `DEC-001` a `DEC-007` y matriz de cobertura de 23 filas |
| 0.4.0 | 2026-11-20 | Tareas cerradas: 19 tareas atómicas con dependencias acíclicas, evidencia por tarea y trazabilidad `CA-NNN` a `T-NNN` |
| 0.5.0 | 2026-11-20 | Implementación del cierre de la auditoría posterior |
| 0.6.0 | 2026-11-20 | Cierre de la implementación y verificación G3 |
| 0.7.0 | 2026-11-20 | Validación e integración del cierre de la auditoría posterior |
| 0.8.0 | 2026-11-21 | Release v0.7.1 |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-20 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con once requisitos funcionales, cuatro no funcionales, ocho casos borde y once criterios de aceptación |
| 2026-11-20 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con 11 hallazgos resueltos y sin casillas pendientes, y parches aplicados a `spec.md` |
| 2026-11-20 | T2 | `clarified` | `planned` | `planner` | `plan.md` redactado con doce componentes, los contratos `C-1` a `C-8`, las decisiones `DEC-001` a `DEC-007`, la estrategia de testing y la matriz de cobertura de los 11 requisitos funcionales, los 4 no funcionales y los 8 casos borde |
| 2026-11-20 | T3 | `planned` | `tasked` | `planner` | `tasks.md` redactado con 19 tareas atómicas, ocho campos por tarea, dependencias acíclicas y cobertura de los 11 requisitos funcionales, los 4 no funcionales, los 8 casos borde y los 11 criterios de aceptación |
| 2026-11-20 | T4 | `tasked` | `implementing` | `planner` | G2 verificada por el orquestador, diecinueve tareas cerradas con evidencia y `--all` con código 0 |
| 2026-11-20 | T5 | `implementing` | `implemented` | `planner` | G3 verificada en el commit `9750fed` con diecinueve tareas cerradas, 187 pruebas en la suite del mecanismo y 48 en las herramientas de Git |
| 2026-11-20 | T6 | `implemented` | `validated` | `planner` | G4 firmada en el commit `3a98f2b`, dictamen `CONVERGIDO` de 23 de 23 filas e integración `4dd07f5` con dos padres y rama eliminada |
| 2026-11-21 | T7 | `validated` | `released` | `planner` | release v0.7.1 publicado con tag anotado verificado sobre el commit de empaquetado y G6 firmada |
