---
id: SPEC-016
title: Cierre de la auditoría de v0.7.1
status: implemented
version: 0.7.0
created: 2026-11-21
updated: 2026-11-21
owner: Agent Sebaxtian
branch: feat/cierre-auditoria-v0-7-1
release: ""
supersedes: ""
superseded_by: ""
---

# Cierre de la auditoría de v0.7.1

## Contexto y objetivo

El informe `docs/sdd/auditoria_final_v0_7_1.md` evaluó la base normativa v2, las quince specs, el validador, las dos suites, la matriz de agentes, el flujo de integración continua y los registros Git sobre el commit `5ba048d`, y emitió el veredicto global `NO CONFORME` con 11 hallazgos vigentes: 2 observaciones nuevas de severidad Alta, 4 de severidad Media, 1 de severidad Baja y 3 residuos parciales de los diez hallazgos del informe anterior. Las dos observaciones de severidad Alta tienen causas distintas y ambas afectan la independencia de la evidencia: un requisito de la spec auditada fijó el recuento de hallazgos del informe que la audita, y un commit sin firma modificó artefactos ya publicados, entre ellos la entrada del release `v0.7.0` y la regla de firma posterior que ese mismo commit introdujo.

Las nueve observaciones restantes son de alineación normativa, de registro, de autoría o de redacción: el rango 3 y el rango 4 enumeran conjuntos distintos de artefactos de empaquetado y las filas que el empaquetado escribe quedan fuera de su alcance declarado; la entrada del release `v0.7.1` y el reporte de `SPEC-015` no transcriben el resultado de G6 ni el objeto del tag; las 2 filas T7 nombran el commit de empaquetado como destino del tag; la fila del inventario del corpus se escribió fuera del alcance del rol de auditoría; la comprobación del historial de releases conserva una regla más estrecha que el empaquetado; y 2 ramas de empaquetado y 1 archivo sin fila de inventario ya quedaron corregidos y requieren el registro de su cierre con evidencia.

Objetivo: fijar el contrato que cierra las 11 observaciones con el artefacto que satisface cada una y con evidencia verificable, y que elimina la autorreferencia entre una spec y la auditoría que la evalúa, de modo que ningún requisito, criterio o tarea de una spec determine el veredicto, el recuento de hallazgos ni el conjunto de dimensiones de un informe que se emite después de su aprobación.

Resultado esperado: prohibición escrita de la autorreferencia en la norma de rango 3 y en la plantilla de rango 5, con regularización por incremento PATCH de las 2 specs publicadas afectadas; conjunto único de 6 artefactos de empaquetado declarado con el mismo límite en el rango 3 y en el rango 4; ratificación firmada de las 3 modificaciones del commit `564bac4` con alcance declarado y efecto declarativo; registro append-only del resultado de G5 y de G6 y del objeto del tag `v0.7.1` en los 2 soportes; corrección de las 2 filas T7 con el commit de merge publicado como destino del tag; cauce escrito de la fila de inventario a cargo del `documenter`; regularización de la comprobación del historial de releases con fila en el registro de cambios; y tabla de cierre con 1 fila por observación, su artefacto y su evidencia.

La feature no reescribe historia publicada, no mueve ni recrea los tags `v0.7.0` y `v0.7.1`, no cambia los requisitos de las specs publicadas más allá de las 2 filas T7, las 3 notas append-only y las filas de motivo de regularización declaradas, y no emite veredicto de conformidad: el veredicto corresponde al rol de auditoría y el cierre de esta spec se acredita con artefacto y evidencia por observación. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen.

### Ampliación del contrato sobre el inventario y el veredicto

El informe `docs/sdd/auditoria_final_v0_7_1.md` dejó 11 hallazgos con estado distinto de cerrado y el corpus conserva 5 hallazgos con estado `cerrado por exención`, de modo que 16 hallazgos no cuentan con cierre acreditado por artefacto. La ausencia de un registro único permite además que el veredicto dependa del criterio de cada pasada y que un juicio sin regla citada compute como hallazgo. La ampliación fija cuatro piezas: el inventario único de los hallazgos emitidos por los 5 informes de `docs/sdd/`; el criterio que separa hallazgo de observación por la regla normativa citada; el cálculo del veredicto desde el inventario con la definición de `CONFORME`; y la ratificación firmada del propietario para las violaciones históricas que ningún artefacto repara.

Resultado esperado de la ampliación: 1 fila por hallazgo en `docs/sdd/inventario_hallazgos.md` con los 8 campos de `RF-011`; 0 hallazgos sin regla normativa citada; veredicto determinista con 0 hallazgos abiertos bajo `CONFORME`; ratificación firmada de las 5 exenciones y de las 2 modificaciones sin firma, con efecto retroactivo limitado al régimen; y release v0.7.2 condicionado a 1 auditoría sobre el estado integrado con veredicto `CONFORME`.

Los 16 hallazgos del cierre son 11 con estado distinto de cerrado en el informe de v0.7.1 —`AUD-088`, `AUD-089`, `AUD-090`, `AUD-103`, `AUD-104`, `AUD-105`, `AUD-106`, `AUD-107`, `AUD-108`, `AUD-109` y `AUD-110`— y 5 con estado `cerrado por exención` —`AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053`—. Los 11 se cierran con los artefactos de `RF-001` a `RF-010` y con la evidencia de la tabla de cierre de `RF-009`; los 5 se cierran con la ratificación de `RF-014` y con la fila del inventario que declara el estado `cerrado por ratificación`.

### Trazabilidad de los dieciséis hallazgos del inventario

El informe de origen se declara por su nombre de archivo en `docs/sdd/`.

| Hallazgo | Estado en el informe de origen | Requisito | Criterio de aceptación |
|---|---|---|---|
| `AUD-003` | cerrado por exención | `RF-014` | `CA-015` |
| `AUD-004` | cerrado por exención | `RF-014` | `CA-015` |
| `AUD-005` | cerrado por exención | `RF-014` | `CA-015` |
| `AUD-037` | cerrado por exención | `RF-014` | `CA-015` |
| `AUD-053` | cerrado por exención | `RF-014` | `CA-015` |
| `AUD-088` | parcial | `RF-010` | `CA-010` |
| `AUD-089` | parcial | `RF-005` | `CA-005` |
| `AUD-090` | parcial | `RF-014`, `RF-004` | `CA-015`, `CA-004` |
| `AUD-103` | vigente | `RF-003` | `CA-003` |
| `AUD-104` | vigente | `RF-004`, `RF-014` | `CA-004`, `CA-015` |
| `AUD-105` | vigente | `RF-005` | `CA-005` |
| `AUD-106` | vigente | `RF-008` | `CA-008` |
| `AUD-107` | vigente | `RF-008` | `CA-008` |
| `AUD-108` | vigente | `RF-006` | `CA-006` |
| `AUD-109` | vigente | `RF-001`, `RF-002` | `CA-001`, `CA-002` |
| `AUD-110` | vigente | `RF-007` | `CA-007` |

Cada uno de los 16 hallazgos consta con al menos 1 requisito y 1 criterio. El inventario de `RF-011` conserva el estado vigente de cada fila, `RF-012` separa el hallazgo de la observación y `RF-013` calcula el veredicto desde ese estado.

### Trazabilidad con el informe de auditoría

| Observación | Severidad | Requisito | Criterio de aceptación |
|---|---|---|---|
| `AUD-088` | Alta (parcial) | `RF-003`, `RF-010` | `CA-003`, `CA-010` |
| `AUD-089` | Media (parcial) | `RF-005` | `CA-005` |
| `AUD-090` | Alta (parcial) | `RF-004`, `RF-014` | `CA-004`, `CA-015` |
| `AUD-103` | Media | `RF-003` | `CA-003` |
| `AUD-104` | Alta | `RF-004`, `RF-014` | `CA-004`, `CA-015` |
| `AUD-105` | Media | `RF-005` | `CA-005` |
| `AUD-106` | Media | `RF-008` | `CA-008` |
| `AUD-107` | Media | `RF-008` | `CA-008` |
| `AUD-108` | Baja | `RF-006` | `CA-006` |
| `AUD-109` | Alta | `RF-001`, `RF-002` | `CA-001`, `CA-002` |
| `AUD-110` | Media | `RF-007` | `CA-007` |
| Las 11 observaciones | Alta, Media y Baja | `RF-009` | `CA-009` |

Cada una de las 11 observaciones queda cubierta por al menos 1 requisito funcional y por al menos 1 criterio de aceptación. Los requisitos no funcionales y los casos borde completan las condiciones de cierre y no responden a una observación aislada.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`, emite la ratificación firmada de las modificaciones del commit `564bac4` y de las violaciones históricas no reparables con el alcance declarado, firma cada modificación de un artefacto publicado, declara G6 en la entrada del release y declara G6 del release v0.7.2 sobre un informe con veredicto `CONFORME`; no delega la firma.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de `specs/016-cierre-auditoria-v0-7-1/`, escribe la fila de `specs/INDEX.md`, las transiciones T1 a T3 y las transiciones T4 a T7 sobre la verificación registrada por el orquestador; no escribe fuera de `specs/`, no redacta reporte de validación y no declara compuertas.
- **Agente `documenter`:** redacta las correcciones de `docs/sdd/PROTOCOLO_OPERATIVO.md`, de `docs/Flujo_de_Trabajo_Git.md`, de `docs/sdd/plantillas/spec.md`, de `docs/sdd/plantillas/informe_auditoria.md`, de `docs/sdd/inventario_hallazgos.md`, de `docs/sdd/README.md` y de `CHANGELOG.md` dentro del alcance declarado y como delegado explícito del propietario; es el único rol que escribe la fila de inventario de un informe de auditoría y la fila de hallazgo del inventario, y no modifica la sección de aprobaciones de una spec.
- **Agente `coder`:** escribe en `tools/` las comprobaciones de igualdad de los 6 artefactos de empaquetado, de la prohibición de autorreferencia, del inventario previo a la integración del informe, de la regla normativa citada en cada hallazgo y del cálculo del veredicto desde el inventario, regulariza la comprobación del historial de releases y cierra tareas en `tasks.md` con la evidencia transcrita.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec y, por delegación escrita del propietario, escribe las notas append-only de los reportes publicados de `SPEC-013` y de `SPEC-015`, sin alterar matriz ni dictamen; no declara G4.
- **Orquestador (`sdd`):** verifica G2, G3 y G5, registra el resultado de cada verificación, ejecuta el validador y `git add` y `git commit` de los artefactos de control; no redacta artefacto alguno y no declara aprobación.
- **Agente `auditor`:** produce su informe de auditoría con lectura de la base completa y escritura limitada a ese informe, calcula el veredicto desde el estado de las filas del inventario conforme a `RF-013` y cita la regla normativa incumplida en cada hallazgo; no escribe la fila de inventario de su informe, no escribe la fila de hallazgo, no edita requisitos y no declara compuertas.

## Requisitos funcionales (EARS)

### RF-001

`El sistema DEBE fijar en §16 de docs/sdd/PROTOCOLO_OPERATIVO.md la prohibición de que una spec determine el veredicto, el recuento de hallazgos o el conjunto de dimensiones de un informe de auditoría posterior a su aprobación, DEBE declarar la misma prohibición en la lista de prohibiciones de docs/sdd/plantillas/spec.md, DEBE limitar el criterio de aceptación que invoca una auditoría a exigir la existencia del artefacto y la evidencia transcrita, y NO DEBE admitir un requisito, un criterio ni una tarea que declare conforme, no conforme o un recuento de hallazgos de un informe cuya emisión es posterior a la aprobación de la spec.`

### RF-002

`CUANDO una spec publicada conserva un requisito o un criterio que fija el veredicto o el recuento de un informe de auditoría, el sistema DEBE añadir a su reporte de validación 1 nota append-only que transcriba la regla de RF-001 y que declare que el veredicto y el recuento los emite el rol de auditoría, DEBE incrementar la versión de esa spec en 1 incremento PATCH y declarar la versión resultante en 1 fila de motivo por corrección aplicada, DEBE conservar el texto publicado del requisito, del criterio, de la matriz de trazabilidad y del dictamen, y NO DEBE declarar superado un criterio ni alterar el destino released ni el campo release de la spec.`

Specs publicadas afectadas y filas que conservan la forma anterior:

| Spec | Requisito y criterio afectados | Versión de origen | Versión resultante |
|---|---|---|---|
| `SPEC-013` | `RNF-001` y `CA-015` | 0.8.0 | 0.8.1 |
| `SPEC-015` | `RF-010` y `CA-008` | 0.8.0 | 0.8.1 |

### RF-003

`El sistema DEBE declarar en §15 de docs/sdd/PROTOCOLO_OPERATIVO.md los 6 artefactos de empaquetado de la tabla de este requisito con su modificación admitida, DEBE declarar en el paso 3 de docs/Flujo_de_Trabajo_Git.md el mismo conjunto con los mismos 6 límites, DEBE escribir la enumeración del rango 3 antes que la del rango 4 conforme al orden de precedencia, DEBE exigir una spec previa o un fix previo para cualquiera de las rutas restantes, y NO DEBE admitir en la rama release/vX-Y-Z una ruta distinta de los 6 artefactos.`

Artefactos admitidos en la rama de empaquetado:

| N.º | Artefacto | Modificación admitida |
|---|---|---|
| 1 | `CHANGELOG.md` | entrada del release e historial de releases |
| 2 | `specs/INDEX.md` | fila de la spec publicada |
| 3 | `spec.md` de una spec publicada | campos del frontmatter `status`, `version`, `updated` y `release` |
| 4 | `spec.md` de una spec publicada | fila del historial de cambios de la versión de release |
| 5 | `spec.md` de una spec publicada | fila T7 del historial de transiciones |
| 6 | `validation_report.md` de una spec publicada | línea `Release:` con el tag del release |

### RF-004

`CUANDO el propietario ratifica las modificaciones de un commit sin firma verificable sobre artefactos publicados, el sistema DEBE registrar la ratificación en 1 commit firmado por una clave de docs/sdd/firmantes_autorizados, DEBE declarar en la entrada Unreleased de CHANGELOG.md el identificador del commit ratificado, las 3 rutas publicadas que ese commit modificó y el efecto declarativo de la ratificación, DEBE transcribir en la evidencia de cierre el estado de firma del commit de ratificación y la huella de la clave firmante, y NO DEBE modificar el contenido publicado que el commit ratificado introdujo ni reescribir el historial de releases.`

Cierre del caso del commit `564bac4`: las 3 rutas publicadas que modificó son la entrada `v0.7.0` de `CHANGELOG.md`, la fila T7 del historial de transiciones de `SPEC-014` y la nota del reporte de validación de `SPEC-013`. La ratificación declara su alcance, su fecha y el efecto declarativo: el contenido publicado se conserva, la autoría del propietario queda acreditada por la firma del commit de ratificación y la modificación sin firma deja de estar vigente como causa.

### RF-005

`El sistema DEBE añadir al reporte de validación de SPEC-015 1 nota append-only que transcriba el resultado de G5 y de G6 y el objeto anotado del tag v0.7.1 con su mensaje y su commit objetivo, DEBE añadir a la entrada v0.7.1 de CHANGELOG.md 1 bloque de registro con el resultado de G5 y de G6 y con el objeto del tag, DEBE conservar la matriz de trazabilidad, el dictamen y la línea de aprobación de G6 de esos 2 artefactos, y NO DEBE declarar compuerta alguna.`

### RF-006

`El sistema DEBE corregir la evidencia de la fila T7 del historial de transiciones de SPEC-014 y de la fila T7 del historial de transiciones de SPEC-015 para declarar que el tag anotado apunta al commit de merge publicado en main, DEBE declarar el identificador de ese commit y su relación de ancestría con el commit de empaquetado, DEBE conservar el destino released, el campo release y el identificador del release en las 2 filas, y NO DEBE declarar el commit de empaquetado como destino del tag.`

### RF-007

`CUANDO se integra un informe de auditoría en docs/sdd/, el sistema DEBE exigir que la fila del informe en la tabla de inventario de docs/sdd/README.md esté registrada por el rol documenter antes de la integración, DEBE declarar ese cauce en §12 de docs/sdd/PROTOCOLO_OPERATIVO.md y en la sección de inventario de docs/sdd/plantillas/informe_auditoria.md, DEBE limitar la escritura del rol de auditoría al informe que produce, y NO DEBE atribuir al rol de auditoría la escritura de la fila.`

Cierre del caso de la fila 34 de la tabla de inventario, introducida en un commit sin firma verificable: la fila se conserva, su escritura se atribuye a la sesión del propietario y no al rol de auditoría, y el cauce de `documenter` rige desde esta spec para la fila de cada informe.

### RF-008

`El sistema DEBE registrar el cierre de AUD-106 con la evidencia del listado de ramas locales que no conserva release/v0-7-0 ni release/v0-7-1, DEBE registrar el cierre de AUD-107 con la fila de docs/sdd/auditoria_final_v0_7_1.md en la tabla de inventario del corpus, con el número de fila que la tabla declara, y con el resultado de la suite de pruebas del corpus, y NO DEBE declarar cerrada una observación cuyo artefacto o cuya evidencia falte en el commit validado.`

### RF-009

`El sistema DEBE registrar en la tabla de cierre de esta spec 1 fila por cada una de las 11 observaciones AUD-088, AUD-089, AUD-090, AUD-103, AUD-104, AUD-105, AUD-106, AUD-107, AUD-108, AUD-109 y AUD-110, con el artefacto que la cierra y la evidencia transcrita por ruta y línea, DEBE declarar el estado de una fila como cerrado solo cuando su artefacto conste en el commit validado, y NO DEBE condicionar el cierre a la emisión de un informe de auditoría posterior ni declarar el veredicto ni la conformidad del régimen.`

### RF-010

`El sistema DEBE regularizar la comprobación del historial de releases del mecanismo de control para que admita las filas de historial de cambios y de transición que el empaquetado escribe y la constante de estados que admite released, DEBE registrar la regularización en 1 fila del registro de cambios bajo Unreleased, y NO DEBE declarar conforme una comprobación cuya regla siga siendo más estrecha que el alcance de RF-003.`

### RF-011

`El sistema DEBE mantener en docs/sdd/inventario_hallazgos.md 1 fila por cada hallazgo emitido por los 5 informes de auditoría de docs/sdd/, con los 8 campos de la tabla de este requisito, DEBE conservar el identificador AUD-NNN de cada hallazgo sin reutilizarlo ni renumerarlo, DEBE registrar el estado vigente con el informe que lo declara y la evidencia de cierre por ruta y línea, y NO DEBE admitir la integración de un informe de auditoría cuya fila falte ni la de un hallazgo sin fila en el inventario.`

Campos obligatorios de cada fila del inventario:

| N.º | Campo | Contenido obligatorio |
|---|---|---|
| 1 | Identificador | `AUD-NNN` del informe de origen, conservado sin reutilización |
| 2 | Dimensión | D1 a D11 del informe de origen |
| 3 | Severidad | `Crítica`, `Alta`, `Media` o `Baja` |
| 4 | Informe de origen | ruta del informe que emitió el hallazgo y fecha de corte |
| 5 | Regla normativa citada | ruta, capítulo y línea de la regla que se incumple |
| 6 | Estado | `cerrado`, `parcial`, `vigente`, `cerrado por exención` o `cerrado por ratificación` |
| 7 | Evidencia de cierre | ruta y línea del artefacto, o identificador del commit firmado que ratifica |
| 8 | Informe que declara el estado | ruta del informe y fecha de corte |

El documento `docs/sdd/inventario_hallazgos.md` consta en la tabla de inventario de `docs/sdd/README.md` conforme a la regla de inventario del corpus.

### RF-012

`CUANDO el rol de auditoría emite un juicio sobre el régimen, el sistema DEBE exigir que el hallazgo cite la regla normativa que se incumple con su ruta, su capítulo y su línea, DEBE registrar como observación el juicio que no cita una regla, DEBE excluir la observación del recuento de hallazgos y NO DEBE admitir un hallazgo sin regla citada ni un veredicto que compute la observación como hallazgo abierto.`

### RF-013

`El sistema DEBE calcular el veredicto de auditoría desde el estado de las filas del inventario de hallazgos con la condición de la tabla de este requisito, DEBE declarar CONFORME solo cuando el número de hallazgos abiertos sea 0 y el número de observaciones de severidad Alta o Media sin tratamiento sea 0, DEBE aplicar la precedencia NO CONFORME, después NO VERIFICABLE, después PARCIAL y después CONFORME, y NO DEBE admitir un veredicto que contradiga el recuento del inventario.`

Condición de cada veredicto:

| Veredicto | Condición sobre el inventario |
|---|---|
| `NO CONFORME` | 1 o más hallazgos abiertos de severidad `Crítica` o `Alta` |
| `NO VERIFICABLE` | 0 hallazgos abiertos de severidad `Crítica` o `Alta`, y 1 o más filas sin regla normativa citada o sin evidencia de cierre |
| `PARCIAL` | 0 hallazgos abiertos de severidad `Crítica` o `Alta`, 0 filas sin regla citada o sin evidencia de cierre, y 1 o más hallazgos abiertos de severidad `Media` o `Baja`, o 1 o más observaciones de severidad `Alta` o `Media` sin tratamiento |
| `CONFORME` | 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento |

Son estados cerrados `cerrado` y `cerrado por ratificación`; son estados abiertos `parcial`, `vigente` y `cerrado por exención`. Un tratamiento es la decisión registrada del propietario, con fecha e identificador del commit, que declara el efecto de la observación y su destino.

### RF-014

`CUANDO una violación histórica del régimen no admite cierre por artefacto verificable, el sistema DEBE cerrarla mediante 1 ratificación firmada del propietario con una clave de docs/sdd/firmantes_autorizados, DEBE declarar en la ratificación el alcance, la fecha, las rutas o los identificadores afectados y el efecto retroactivo limitado al régimen, DEBE registrar el estado cerrado por ratificación en la fila del inventario con el identificador del commit, y NO DEBE reescribir el contenido publicado ni alterar el informe que emitió el hallazgo.`

Casos de esta spec: las 5 exenciones `AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053`, y las 2 modificaciones sin firma de los commits `494db2e` y `564bac4`. `RF-004` registra la ratificación del segundo y `RF-014` declara el efecto común de la ratificación sobre el régimen.

### RF-015

`El sistema DEBE publicar el release v0.7.2 solo después de 1 auditoría de conformidad ejecutada sobre el estado integrado en dev que declare el veredicto CONFORME conforme a RF-013, DEBE transcribir en la entrada del release el identificador del informe y el veredicto, DEBE exigir G5 antes de G6, y NO DEBE publicar el release con 1 hallazgo abierto de severidad Crítica o Alta ni con 1 observación de severidad Alta o Media sin tratamiento.`

## Requisitos no funcionales

### RNF-001

`El número de requisitos, criterios de aceptación y tareas de esta spec que fijan el veredicto, el recuento de hallazgos o el conjunto de dimensiones de un informe de auditoría DEBE ser 0.`

### RNF-002

`El número de requisitos renumerados de las specs publicadas DEBE ser 0 y el 100 % de sus requisitos y de sus criterios DEBE conservarse, con la sola excepción de las 2 filas T7, las 3 notas append-only y las filas de motivo de regularización que RF-002, RF-005 y RF-006 declaran.`

### RNF-003

`La validación agregada DEBE completar en 300 segundos o menos sobre el commit validado.`

### RNF-004

`El número de artefactos publicados modificados por esta spec fuera de 1 commit firmado por una clave de docs/sdd/firmantes_autorizados DEBE ser 0.`

### RNF-005

`El número de hallazgos emitidos por los informes de auditoría de docs/sdd/ que carecen de fila en el inventario DEBE ser 0 y el número de campos obligatorios de RF-011 con contenido vacío en una fila DEBE ser 0.`

### RNF-006

`El número de hallazgos del inventario sin regla normativa citada por ruta, capítulo y línea DEBE ser 0.`

### RNF-007

`El número de veredictos que difieren del cálculo de RF-013 para el mismo conjunto de filas DEBE ser 0 y el número de hallazgos abiertos admitidos bajo un veredicto CONFORME DEBE ser 0.`

### RNF-008

`El número de violaciones históricas cerradas sin 1 ratificación firmada por una clave de docs/sdd/firmantes_autorizados DEBE ser 0.`

### RNF-009

`El número de releases publicados con posterioridad a esta spec sin 1 auditoría previa sobre el estado integrado con veredicto CONFORME DEBE ser 0.`

## Casos borde

### CB-001

`SI una de las 11 observaciones carece de artefacto de cierre en el commit validado, ENTONCES el sistema NO DEBE declararla cerrada y DEBE registrar su causa como vigente.`

### CB-002

`SI el commit de ratificación no verifica su firma o su clave no figura en docs/sdd/firmantes_autorizados, ENTONCES la ratificación NO DEBE admitirse y DEBE transcribirse el estado de firma del commit.`

### CB-003

`SI el rango 3 y el rango 4 enumeran conjuntos distintos de artefactos de empaquetado, ENTONCES la verificación DEBE registrar un error que nombre la diferencia y NO DEBE declarar alineada la enumeración.`

### CB-004

`SI la corrección de una fila T7 altera el destino released, el campo release o el identificador del release, ENTONCES la corrección DEBE rechazarse y el conflicto DEBE registrarse en el reporte de la spec afectada.`

### CB-005

`SI el reporte de SPEC-015 ya porta una transcripción del objeto del tag v0.7.1, ENTONCES la nota nueva DEBE añadirse a continuación sin eliminar la anterior y sin alterar la matriz ni el dictamen.`

### CB-006

`SI un requisito o un criterio de una spec fija el veredicto o el recuento de un informe de auditoría, ENTONCES la verificación DEBE registrar el hallazgo y la spec NO DEBE aprobarse en G1.`

### CB-007

`SI un informe de auditoría se integra sin la fila de inventario registrada por el documenter, ENTONCES el check verify DEBE quedar en rojo con la ruta del archivo sin fila y la integración DEBE detenerse.`

### CB-008

`SI un informe posterior declara un estado distinto para un hallazgo que ya figura en el inventario, ENTONCES el sistema DEBE conservar el identificador, DEBE registrar el estado nuevo con el informe que lo declara y su evidencia, y NO DEBE asignar un identificador nuevo al mismo hallazgo.`

### CB-009

`SI un juicio de auditoría no cita la regla normativa que se incumple, ENTONCES el sistema DEBE registrarlo como observación, DEBE excluirlo del recuento de hallazgos y NO DEBE computar su severidad como hallazgo abierto en el cálculo del veredicto.`

### CB-010

`SI el recuento del inventario produce un veredicto distinto del que declara el informe, ENTONCES la verificación DEBE registrar el error con la fila que sostiene la diferencia y NO DEBE admitir el veredicto declarado.`

### CB-011

`SI una violación histórica no admite cierre por artefacto verificable, ENTONCES el sistema DEBE exigir 1 ratificación firmada del propietario con alcance y efecto declarados, DEBE limitar el efecto retroactivo al régimen y NO DEBE reescribir el contenido publicado.`

### CB-012

`SI la auditoría previa al release v0.7.2 emite un veredicto distinto de CONFORME, ENTONCES el sistema NO DEBE publicar el release, DEBE conservar la spec en validated y DEBE transcribir el motivo con el hallazgo que lo sostiene.`

### CB-013

`SI un archivo de informe de auditoría consta en docs/sdd/ sin fila en el inventario de hallazgos, ENTONCES la verificación DEBE quedar en rojo con la ruta del archivo y la integración DEBE detenerse.`

## Fuera de alcance

- La reescritura de historia publicada, con rebase, squash o copia manual de commits integrados.
- El movimiento, la recreación o la eliminación de los tags `v0.7.0` y `v0.7.1`.
- El cambio de requisitos o de criterios de las specs publicadas más allá de las 2 filas T7, las 3 notas append-only y las filas de motivo de regularización declaradas.
- La modificación de `docs/sdd/auditoria_final_v0_7_1.md`: se cita como evidencia y no se modifica.
- El cambio de la regla de firma posterior a la publicación: se aplica sin alteración.
- La ampliación de las 2 ventanas de legado de §14 del protocolo.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.
- La emisión de un veredicto de conformidad del régimen, que corresponde al rol de auditoría.
- La publicación del release v0.7.2: esta spec fija su condición y no lo publica.
- La modificación de los informes de auditoría publicados: se citan como evidencia y no se reescriben.
- La reasignación del identificador de un hallazgo ya emitido y la reapertura de un hallazgo cerrado sin un informe que declare el estado nuevo.
- Hardware, modelos, cuantizaciones y benchmarks de ejecución local.

## Criterios de aceptación

### CA-001

`DADOS §16 de docs/sdd/PROTOCOLO_OPERATIVO.md, la lista de prohibiciones de docs/sdd/plantillas/spec.md y la separación entre spec y auditoría, CUANDO se contrastan las 2 declaraciones con un criterio de aceptación que invoca una auditoría, ENTONCES §16 declara que ninguna spec fija el veredicto, el recuento de hallazgos ni el conjunto de dimensiones de un informe posterior a su aprobación, la plantilla declara la misma prohibición, el criterio se limita a exigir la existencia del artefacto y la evidencia transcrita, y una spec con un requisito o un criterio que fija el veredicto o el recuento queda registrada con el hallazgo y no se aprueba en G1.`

Cubre: `RF-001`, `CB-006`.

### CA-002

`DADAS SPEC-013 y SPEC-015, CUANDO se aplica la regularización de la autorreferencia, ENTONCES cada reporte de validación porta 1 nota append-only con la regla de RF-001 y con la declaración de que el veredicto y el recuento los emite el rol de auditoría, cada spec incrementa 1 incremento PATCH hasta la versión resultante de la tabla de RF-002 con 1 fila de motivo por corrección aplicada, y el requisito, el criterio, la matriz, el dictamen, el destino released y el campo release conservan su texto publicado.`

Cubre: `RF-002`.

### CA-003

`DADOS §15 de docs/sdd/PROTOCOLO_OPERATIVO.md, el paso 3 de docs/Flujo_de_Trabajo_Git.md y el empaquetado de v0.7.1, CUANDO se contrastan las 2 enumeraciones, ENTONCES las 2 declaran los 6 artefactos de la tabla de RF-003 con los mismos 6 límites, el rango 3 se escribe antes que el rango 4, cualquier ruta distinta exige una spec previa o un fix previo, y una diferencia entre las 2 enumeraciones produce un error que la nombra sin declarar alineada la enumeración.`

Cubre: `RF-003`, `CB-003`.

### CA-004

`DADO el commit 564bac4, que modificó la entrada v0.7.0 de CHANGELOG.md, la fila T7 de SPEC-014 y la nota del reporte de SPEC-013 sin firma verificable, CUANDO el propietario ratifica sus modificaciones, ENTONCES la ratificación consta en 1 commit firmado con una clave de docs/sdd/firmantes_autorizados, la entrada Unreleased declara el identificador 564bac4, las 3 rutas y el efecto declarativo, la evidencia de cierre transcribe el estado de firma y la huella de la clave, el contenido publicado se conserva sin modificación, y una ratificación sin firma verificable no se admite.`

Cubre: `RF-004`, `CB-002`.

### CA-005

`DADOS el reporte de validación de SPEC-015 y la entrada v0.7.1 de CHANGELOG.md, CUANDO se registra el resultado del release, ENTONCES el reporte porta 1 nota append-only con el resultado de G5 y de G6 y con el objeto anotado del tag v0.7.1, su mensaje y su commit objetivo, la entrada porta 1 bloque de registro con ese resultado y ese objeto, la matriz, el dictamen y la línea de aprobación de G6 se conservan, una transcripción previa del objeto se conserva con la nota nueva a continuación, y ninguna de las 2 escrituras declara compuerta.`

Cubre: `RF-005`, `CB-005`.

### CA-006

`DADAS las filas T7 de SPEC-014 y de SPEC-015, CUANDO se corrige su evidencia, ENTONCES cada fila declara el commit de merge publicado en main como destino del tag anotado, declara su identificador y su relación de ancestría con el commit de empaquetado, conserva el destino released, el campo release y el identificador del release, y una corrección que altere el destino, el campo release o el identificador del release se rechaza con el conflicto registrado en el reporte de la spec afectada.`

Cubre: `RF-006`, `CB-004`.

### CA-007

`DADOS el rol de auditoría, la tabla de inventario de docs/sdd/README.md y el informe docs/sdd/auditoria_final_v0_7_1.md, CUANDO se integra un informe de auditoría, ENTONCES la fila del informe consta en la tabla de inventario y la escribe el rol documenter antes de la integración, §12 del protocolo y la plantilla del informe declaran ese cauce, la escritura del rol de auditoría se limita al informe, la fila no se le atribuye, y un informe integrado sin fila deja el check verify en rojo con la ruta del archivo sin fila.`

Cubre: `RF-007`, `CB-007`.

### CA-008

`DADOS AUD-106 y AUD-107, CUANDO se registra su cierre, ENTONCES el cierre de AUD-106 transcribe el listado de ramas locales sin release/v0-7-0 ni release/v0-7-1, el cierre de AUD-107 transcribe la fila de docs/sdd/auditoria_final_v0_7_1.md con el número de fila que la tabla declara y el resultado de la suite de pruebas del corpus, y una observación con artefacto o con evidencia ausente queda registrada como vigente y no como cerrada.`

Cubre: `RF-008`, `CB-001`.

### CA-009

`DADAS las 11 observaciones del informe de auditoría de v0.7.1, CUANDO se contrasta la tabla de cierre de esta spec, ENTONCES figura 1 fila por observación con el artefacto que la cierra y la evidencia transcrita por ruta y línea, el estado cerrado figura solo en las filas cuyo artefacto consta en el commit validado, y el cierre no depende de un informe de auditoría posterior ni declara veredicto de conformidad.`

Cubre: `RF-009`, `CB-001`.

### CA-010

`DADOS el mecanismo de control y el registro de cambios, CUANDO se contrasta la regularización de la comprobación del historial de releases, ENTONCES la comprobación admite las filas de historial de cambios y de transición que el empaquetado escribe y la constante de estados que admite released, la regularización consta en 1 fila del registro de cambios bajo Unreleased, y ninguna comprobación se declara conforme con una regla más estrecha que el alcance de RF-003.`

Cubre: `RF-010`.

### CA-011

`DADO el commit validado, CUANDO se ejecuta la validación agregada y se contrastan las specs publicadas con su versión anterior, ENTONCES el número de requisitos, criterios y tareas de esta spec que fijan el veredicto, el recuento o las dimensiones de un informe de auditoría es 0, el número de requisitos renumerados es 0 y el 100 % de sus requisitos y criterios se conserva con las excepciones declaradas, la ejecución completa en 300 segundos o menos, y el número de artefactos publicados modificados fuera de 1 commit firmado es 0.`

Cubre: `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004`.

### CA-012

`DADOS los 5 informes de auditoría de docs/sdd/ y el documento docs/sdd/inventario_hallazgos.md, CUANDO se contrasta el inventario con los hallazgos emitidos, ENTONCES cada hallazgo AUD-NNN consta en 1 fila con los 8 campos de RF-011, el identificador se conserva sin reutilización ni renumeración, el estado vigente y su evidencia constan con el informe que los declara, un estado nuevo se registra sobre el identificador existente, y un informe integrado sin fila o un hallazgo sin fila deja la verificación en rojo con la ruta del archivo y detiene la integración.`

Cubre: `RF-011`, `CB-008`, `CB-013`.

### CA-013

`DADO un juicio emitido por el rol de auditoría, CUANDO se contrasta con la regla normativa que declara incumplida, ENTONCES el hallazgo cita la ruta, el capítulo y la línea de la regla, el juicio que no cita una regla consta como observación, la observación queda fuera del recuento de hallazgos, y su severidad no computa como hallazgo abierto en el cálculo del veredicto.`

Cubre: `RF-012`, `CB-009`.

### CA-014

`DADO el inventario de hallazgos y la condición de cálculo de RF-013, CUANDO se calcula el veredicto sobre el corte auditado, ENTONCES el veredicto coincide con la condición de la tabla para el recuento de hallazgos abiertos y de observaciones sin tratamiento, la precedencia NO CONFORME, NO VERIFICABLE, PARCIAL y CONFORME se aplica en ese orden, CONFORME exige 0 hallazgos abiertos y 0 observaciones de severidad Alta o Media sin tratamiento, y un veredicto que contradiga el recuento se registra con la fila que sostiene la diferencia.`

Cubre: `RF-013`, `CB-010`.

### CA-015

`DADA una violación histórica sin cierre por artefacto verificable, CUANDO el propietario la ratifica, ENTONCES la ratificación consta en 1 commit firmado con una clave de docs/sdd/firmantes_autorizados, declara el alcance, la fecha, las rutas o los identificadores afectados y el efecto retroactivo limitado al régimen, la fila del inventario pasa a cerrado por ratificación con el identificador del commit, y el contenido publicado y el informe de origen conservan su texto.`

Cubre: `RF-014`, `CB-011`.

### CA-016

`DADO el release v0.7.2 y el estado integrado en dev, CUANDO se prepara su publicación, ENTONCES consta 1 auditoría ejecutada sobre el estado integrado con veredicto CONFORME conforme a RF-013, la entrada del release transcribe el identificador del informe y el veredicto, G5 precede a G6, y un veredicto distinto de CONFORME impide la publicación, conserva la spec en validated y transcribe el motivo con el hallazgo que lo sostiene.`

Cubre: `RF-015`, `CB-012`.

### CA-017

`DADO el commit validado, CUANDO se ejecutan las verificaciones de los criterios de RF-011 a RF-015, ENTONCES el número de hallazgos sin fila en el inventario es 0, el número de campos obligatorios vacíos por fila es 0, el número de hallazgos sin regla normativa citada es 0, el número de veredictos que difieren del cálculo del inventario es 0, el número de hallazgos abiertos admitidos bajo un veredicto CONFORME es 0, el número de violaciones históricas cerradas sin ratificación firmada es 0 y el número de releases publicados sin auditoría previa con veredicto CONFORME es 0.`

Cubre: `RNF-005`, `RNF-006`, `RNF-007`, `RNF-008`, `RNF-009`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-21)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-21 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-21 | Clarificación cerrada: 10 ambigüedades resueltas y parches aplicados a los requisitos funcionales, los requisitos no funcionales, los casos borde, los criterios de aceptación, los actores y el alcance |
| 0.3.0 | 2026-11-21 | Ampliación de la clarificación: 6 ambigüedades resueltas y parches aplicados al inventario de hallazgos, al criterio que separa hallazgo de observación, al cálculo del veredicto, a la ratificación de las violaciones históricas y a la condición del release v0.7.2 |
| 0.4.0 | 2026-11-21 | Plan técnico: 12 componentes, los contratos `C-1` a `C-9`, las decisiones `DEC-001` a `DEC-008`, la estrategia de testing y la matriz de cobertura de los 15 requisitos funcionales, los 9 requisitos no funcionales y los 13 casos borde |
| 0.5.0 | 2026-11-21 | Descomposición en tareas: 34 tareas atómicas con los ocho campos, dependencias acíclicas y cobertura de los 15 requisitos funcionales, los 9 requisitos no funcionales, los 13 casos borde y los 17 criterios de aceptación |
| 0.6.0 | 2026-11-21 | Implementación del cierre de la auditoría de v0.7.1 |
| 0.7.0 | 2026-11-21 | Cierre de la implementación y verificación G3 |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-21 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con diez requisitos funcionales, cuatro no funcionales, siete casos borde y once criterios de aceptación |
| 2026-11-21 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con 10 hallazgos resueltos y sin casillas pendientes, y parches aplicados a `spec.md` |
| 2026-11-21 | T2 | `clarified` | `planned` | `planner` | G1 firmada en `spec.md` y `plan.md` redactado con 12 componentes, los contratos `C-1` a `C-9`, las decisiones `DEC-001` a `DEC-008`, la estrategia de testing y la matriz de cobertura de los 15 requisitos funcionales, los 9 requisitos no funcionales y los 13 casos borde |
| 2026-11-21 | T3 | `planned` | `tasked` | `planner` | `tasks.md` redactado con 34 tareas atómicas, ocho campos por tarea, dependencias acíclicas y cobertura de los 15 requisitos funcionales, los 9 requisitos no funcionales, los 13 casos borde y los 17 criterios de aceptación |
| 2026-11-21 | T4 | `tasked` | `implementing` | `planner` | G2 verificada por el orquestador, treinta y cuatro tareas cerradas con evidencia y `--all` con código 0 |
| 2026-11-21 | T5 | `implementing` | `implemented` | `planner` | G3 verificada en el commit `e2ede7a` con treinta y cuatro tareas cerradas, 222 pruebas en la suite del mecanismo y 48 en las herramientas de Git |
