---
id: SPEC-014
title: Cierre de las observaciones de la reauditoría final
status: released
version: 0.8.1
created: 2026-11-14
updated: 2026-11-20
owner: Agent Sebaxtian
branch: feat/cierre-observaciones-finales
release: "v0.7.0"
supersedes: ""
superseded_by: ""
---

# Cierre de las observaciones de la reauditoría final

## Contexto y objetivo

La reauditoría final registrada en `docs/sdd/auditoria_final_v0_7_0.md` evaluó la base normativa v2, las trece specs, el validador, las dos suites, la matriz de agentes, el flujo de integración continua y el historial Git sobre el commit `d490190`. El informe confirmó el cierre de las dieciséis observaciones de `docs/sdd/auditoria_cierre_v0_7_0.md` —quince con artefacto y evidencia y una por exención declarada— y emitió el veredicto global `CONFORME CON OBSERVACIONES`, equivalente a `PARCIAL` en la escala de la plantilla de auditoría, sostenido por siete observaciones nuevas: cinco de severidad Media y dos de severidad Baja.

Tres de esas siete observaciones quedaron cerradas en la integración del Pull Request #13: `AUD-038`, por la incorporación del check `verify` a la condición de G5; `AUD-067`, por la corrección editorial de la atribución del bloque B3; y `AUD-098`, por la fila del informe final en la tabla de inventario del corpus. Quedan abiertas cuatro observaciones: `AUD-066`, porque la matriz del orquestador conserva escritura sobre `.github/**`, `opencode.jsonc` y `MEMORY.md` mientras §12 del protocolo se la niega; `AUD-075`, porque la fila de `RNF-001` y la de `CA-015` de `SPEC-013` figuran superadas con evidencia diferida al informe final y esa evidencia no confirma el veredicto anticipado; `AUD-101`, porque el flujo prepara el árbol sin profundidad completa y sin etiquetas, de modo que la comprobación de la referencia a la spec no examina commit alguno; y `AUD-102`, porque el job `verify` ejecuta solo la suite de `tools/sdd/tests` y las 48 pruebas de `tools/git/tests` no forman parte del check exigible.

Objetivo: fijar el contrato que cierra las cuatro observaciones restantes, de modo que cada una quede cerrada con el artefacto que la satisface y con evidencia verificable, y que la reauditoría posterior encuentre cero observaciones abiertas de las siete del informe final.

Resultado esperado: flujo de integración continua que prepara el árbol con profundidad completa del historial y con las etiquetas del repositorio, de modo que la comprobación de la referencia a la spec examine al menos un commit; job `verify` que ejecuta las dos suites y declara su alcance en la norma de integración; matriz del orquestador limitada a `.opencode/**` y sin contradicción con §12 del protocolo; nota de cierre append-only en el reporte de `SPEC-013` que transcribe el veredicto del informe final sin alterar la matriz ni el dictamen; y declaración de cuatro de cuatro observaciones cerradas.

La feature no reabre requisito alguno de `SPEC-013`, no cambia el estado de esa spec y no altera su matriz de trazabilidad ni su dictamen. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen ni la autorización de un release.

### Trazabilidad con el informe de reauditoría final

| Observación | Severidad | Requisito | Criterio de aceptación |
|---|---|---|---|
| `AUD-101` | Media | `RF-001` | `CA-001` |
| `AUD-102` | Baja | `RF-002` | `CA-002` |
| `AUD-066` | Media | `RF-003` | `CA-003` |
| `AUD-075` | Media | `RF-004` | `CA-004` |
| `AUD-066`, `AUD-075`, `AUD-101`, `AUD-102` | Media y Baja | `RF-005` | `CA-005` |

Cada una de las cuatro observaciones abiertas queda cubierta por un requisito funcional y por al menos un criterio de aceptación. Los requisitos no funcionales y los casos borde completan las condiciones de cierre y no responden a una observación aislada.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`, decide el sentido de cada una de las cuatro observaciones, escribe la reducción de la matriz del orquestador en `.opencode/agents/sdd.md` y en `opencode.jsonc` —rutas sin rol concesionario— y delega por escrito la escritura de la nota de cierre; no delega la firma.
- **Orquestador (`sdd`):** conserva escritura sobre `.opencode/**` y ninguna otra, verifica G2, G3 y G5, registra el resultado de cada verificación, ejecuta el validador y `git add` y `git commit` de los artefactos de control, y no redacta artefacto alguno; no declara aprobación.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de `specs/014-cierre-observaciones-finales/`, escribe las transiciones T4 a T7 sobre la verificación registrada por el orquestador y no escribe fuera de `specs/`; no redacta reporte de validación y no declara compuertas.
- **Agente `coder`:** escribe en `.github/` y en `tools/` la preparación del árbol con profundidad completa y etiquetas, el paso de la segunda suite, las pruebas de la matriz de permisos y las pruebas del flujo, y cierra tareas en `tasks.md` con la evidencia transcrita.
- **Agente `documenter`:** redacta las correcciones de `docs/Flujo_de_Trabajo_Git.md` dentro del alcance declarado y como delegado explícito del propietario para `MEMORY.md` y `CHANGELOG.md`.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec con la matriz de trazabilidad y el dictamen, y escribe la nota de cierre append-only en el reporte de `SPEC-013` por delegación escrita del propietario, sin modificar la matriz ni el dictamen de esa spec; no declara G4.
- **Agente `auditor`:** ejecuta la reauditoría posterior, registra el veredicto por dimensión y el estado de cada observación en el informe de auditoría que produce, y no edita requisitos ni declara compuertas.

## Requisitos funcionales (EARS)

### RF-001

`CUANDO el job `verify` del flujo `SDD` prepara el árbol del repositorio, el sistema DEBE declarar la profundidad completa del historial con el valor 0 en el recorte y DEBE declarar la descarga de las etiquetas del repositorio, de modo que el alcance de la comprobación de la referencia a la spec examine al menos 1 commit de implementación cuando el rango no esté vacío, y NO DEBE conservar una preparación superficial ni una preparación que omita las etiquetas.`

Parámetros fijados de la preparación del árbol:

| Parámetro | Valor exigido |
|---|---|
| Profundidad del historial | `0`, equivalente a historial completo |
| Descarga de etiquetas | habilitada |

### RF-002

`El sistema DEBE ejecutar en el job `verify` del flujo `SDD` las 2 suites de pruebas del repositorio —la suite de `tools/sdd/tests` y la suite de `tools/git/tests`—, DEBE declarar cada ejecución como un paso nombrado del job, DEBE declarar en `docs/Flujo_de_Trabajo_Git.md` que el check `verify` ejecuta las 2 suites, y NO DEBE dejar la suite de `tools/git/tests` fuera de job alguno.`

### RF-003

`El sistema DEBE reducir la matriz de escritura del orquestador a `.opencode/**` como única concesión, DEBE retirar de `.opencode/agents/sdd.md` la concesión de escritura sobre `.github/**`, `opencode.jsonc` y `MEMORY.md`, DEBE conservar en 0 las atribuciones de escritura del orquestador sobre documentos, código y configuración fuera de `.opencode/**`, y NO DEBE mantener contradicción entre la matriz y §12 del protocolo.`

Valores fijados de la matriz del orquestador:

| Ruta | Efecto exigido | Rol concesionario tras la corrección |
|---|---|---|
| `.opencode/**` | `allow` | orquestador |
| `.github/**` | `deny` | `coder` |
| `opencode.jsonc` | `deny` | propietario |
| `MEMORY.md` | `deny` | `documenter` |

### RF-004

`El sistema DEBE añadir al reporte de validación de `SPEC-013` una nota de cierre append-only que transcriba el veredicto `CONFORME CON OBSERVACIONES` del informe `docs/sdd/auditoria_final_v0_7_0.md`, el cierre de las 16 observaciones de la reauditoría previa, la causa del veredicto y el estado de las 4 observaciones que esta spec cierra, DEBE conservar sin alteración la matriz de trazabilidad y el dictamen de esa spec, DEBE conservar su estado `validated`, y NO DEBE reabrir requisito alguno de `SPEC-013`.`

### RF-005

`El sistema DEBE cerrar las 4 observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102` con el artefacto que las satisface y con la evidencia transcrita, DEBE declarar en el informe final 4 de 4 cerradas, y NO DEBE declarar cerrada una observación que conserve causa vigente ni cerrarla sin evidencia.`

## Requisitos no funcionales

### RNF-001

`La validación agregada DEBE completar en 300 segundos o menos sobre el commit validado.`

### RNF-002

`El job `verify` DEBE conservar un límite total de ejecución de 5 minutos o menos y cada paso de suite DEBE declarar un límite propio de 1 minuto o menos.`

### RNF-003

`Cada comprobación nueva DEBE declarar al menos 1 prueba positiva y 1 prueba negativa en la suite del mecanismo de control.`

### RNF-004

`Las correcciones de esta spec DEBEN conservar sin cambios el 100 % de los requisitos, los criterios de aceptación y el estado de `SPEC-013`, y el 100 % de las filas de su matriz de trazabilidad y de su dictamen.`

### RNF-005

`El número de contradicciones entre la matriz de permisos del orquestador y §12 del protocolo sobre las rutas de escritura DEBE ser 0 tras la implementación.`

## Casos borde

### CB-001

`SI la preparación del árbol declara la profundidad completa y omite la descarga de etiquetas, ENTONCES la verificación del flujo DEBE registrar un error que nombre la etiqueta ausente y NO DEBE declarar verificado el alcance de la referencia a la spec.`

### CB-002

`SI el clon del job declara la profundidad completa y el repositorio no declara tag anotado de release, ENTONCES la comprobación de la referencia a la spec DEBE acotar el alcance por el ancestro común con `main` y NO DEBE informar la ausencia de etiquetas como defecto del repositorio.`

### CB-003

`SI la suite de `tools/git/tests` falla en el job `verify`, ENTONCES el check `verify` DEBE quedar en rojo y la verificación de G5 DEBE quedar bloqueada.`

### CB-004

`SI el orquestador intenta escribir una ruta fuera de `.opencode/**`, ENTONCES la matriz DEBE denegar la escritura y el artefacto DEBE quedar atribuido al rol que `tasks.md` declara para esa tarea.`

### CB-005

`SI el reporte de `SPEC-013` ya declara una nota de cierre, ENTONCES la nota nueva DEBE añadirse a continuación sin eliminar la anterior y sin alterar la matriz ni el dictamen.`

### CB-006

`SI la nota de cierre transcribe un estado de las 16 observaciones distinto del que declara el informe final, ENTONCES la validación DEBE registrar un error que nombre el valor en conflicto y NO DEBE declarar la nota conforme.`

### CB-007

`SI una de las 4 observaciones no cuenta con artefacto de cierre, ENTONCES el informe final NO DEBE declararla cerrada y DEBE registrar su causa en estado vigente.`

## Fuera de alcance

- El release `v0.7.0`, su tag y su compuerta G6: se ejecutan después de esta spec y la citan como antecedente.
- El cambio del contenido funcional y del estado de `SPEC-013`: esta spec añade una nota de cierre append-only y conserva su matriz, su dictamen y su estado `validated`.
- La corrección editorial del bloque B3 de la constitución, del protocolo y de la plantilla de auditoría: `AUD-067` quedó cerrada en el Pull Request #13.
- La fila del informe final en la tabla de inventario del corpus: `AUD-098` quedó cerrada en el Pull Request #13.
- La incorporación del check `verify` a la condición de G5: `AUD-038` quedó cerrada en el Pull Request #13.
- La reescritura de `docs/sdd/auditoria_final_v0_7_0.md`: se cita como evidencia y no se modifica.
- La modificación de la matriz de escritura de los roles `planner`, `documenter`, `coder`, `reviewer` y `auditor`.
- La verificación de la configuración remota de protección por una vía distinta de las reglas declaradas en el repositorio.
- La ampliación del alcance del validador a la ejecución real del flujo en GitHub.
- Hardware, modelos, cuantizaciones y benchmarks de ejecución local.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.

## Criterios de aceptación

### CA-001

`DADO el job `verify` del flujo `SDD`, CUANDO se contrasta su preparación del árbol y se inspecciona el alcance de la comprobación de la referencia a la spec, ENTONCES la preparación declara la profundidad completa con el valor 0 y la descarga de etiquetas habilitada, el alcance enumera al menos 1 commit de implementación cuando el rango no está vacío, la omisión de las etiquetas produce un error con la etiqueta ausente, y la ausencia de tag anotado acota el alcance por el ancestro común con `main` sin informar un defecto del repositorio.`

Cubre: `RF-001`, `CB-001`, `CB-002`.

### CA-002

`DADO el job `verify` del flujo `SDD`, CUANDO se ejecuta sobre un Pull Request dirigido a `main` o a `dev`, ENTONCES ejecuta la suite de `tools/sdd/tests` y la suite de `tools/git/tests` como pasos nombrados, `docs/Flujo_de_Trabajo_Git.md` declara que el check `verify` ejecuta las 2 suites, el fallo de la suite de `tools/git/tests` deja el check en rojo y bloquea G5, y ninguna de las 2 suites queda fuera del job.`

Cubre: `RF-002`, `CB-003`.

### CA-003

`DADAS la matriz de permisos y la definición del rol orquestador, CUANDO se contrastan entre sí y con §12 del protocolo, ENTONCES `.opencode/**` es la única ruta con efecto `allow` de escritura, las rutas `.github/**`, `opencode.jsonc` y `MEMORY.md` declaran efecto `deny`, las atribuciones de escritura fuera de `.opencode/**` son 0, la contradicción entre matriz y protocolo es 0 y una escritura intentada fuera de `.opencode/**` queda denegada con el artefacto atribuido al rol declarado.`

Cubre: `RF-003`, `CB-004`.

### CA-004

`DADO el reporte de validación de `SPEC-013`, CUANDO se añade la nota de cierre, ENTONCES la nota figura a continuación de las notas precedentes y transcribe el veredicto `CONFORME CON OBSERVACIONES`, el cierre de las 16 observaciones de la reauditoría previa, la causa del veredicto y el estado de las 4 observaciones de esta spec, la matriz de trazabilidad y el dictamen conservan su contenido, el estado `validated` no cambia, y una nota que transcriba un estado distinto del que declara el informe final produce un error con el valor en conflicto.`

Cubre: `RF-004`, `CB-005`, `CB-006`.

### CA-005

`DADAS las 4 observaciones `AUD-066`, `AUD-075`, `AUD-101` y `AUD-102`, CUANDO se contrastan con su artefacto de cierre y con el informe final, ENTONCES las 4 cuentan con artefacto y evidencia transcrita, el informe final declara 4 de 4 cerradas, y una observación sin artefacto de cierre queda registrada en estado vigente y no se declara cerrada.`

Cubre: `RF-005`, `CB-007`.

### CA-006

`DADO el corpus en el commit validado, CUANDO se ejecuta la validación agregada y se inspecciona el job `verify`, ENTONCES cada ejecución completa en 300 segundos o menos, el job conserva un límite total de 5 minutos o menos y cada paso de suite declara un límite de 1 minuto o menos, y cada comprobación nueva declara al menos 1 prueba positiva y 1 prueba negativa en la suite del mecanismo de control.`

Cubre: `RNF-001`, `RNF-002`, `RNF-003`.

### CA-007

`DADOS `SPEC-013` y la matriz de permisos del orquestador, CUANDO se contrastan con su versión anterior, ENTONCES el 100 % de los requisitos, los criterios de aceptación, el estado, las filas de la matriz de trazabilidad y el dictamen de `SPEC-013` queda sin cambios, y el número de contradicciones entre la matriz de permisos del orquestador y §12 del protocolo sobre las rutas de escritura es 0.`

Cubre: `RNF-004`, `RNF-005`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-14)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación cerrada: 6 ambigüedades resueltas, casos borde `CB-006` y `CB-007` añadidos y parches aplicados a requisitos, casos borde, criterios y actores |
| 0.3.0 | 2026-11-14 | Plan técnico redactado: 6 decisiones `DEC-001` a `DEC-006`, 6 contratos `C-1` a `C-6`, estrategia de testing y matriz de cobertura de 17 filas |
| 0.4.0 | 2026-11-14 | Descomposición en tareas: 13 tareas atómicas con dependencias acíclicas, cobertura completa de `RF`, `RNF` y `CB`, y matriz de tareas y de criterios |
| 0.5.0 | 2026-11-14 | Implementación del cierre de observaciones finales |
| 0.6.0 | 2026-11-14 | Cierre de la implementación y verificación G3 |
| 0.7.0 | 2026-11-14 | Validación e integración del cierre de observaciones finales |
| 0.8.0 | 2026-11-14 | Release v0.7.0 |
| 0.8.1 | 2026-11-20 | Corrección de la fila T7: release v0.7.0 publicado |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con cinco requisitos funcionales, cinco no funcionales, cinco casos borde y siete criterios de aceptación |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con 6 hallazgos resueltos y sin casillas pendientes, y parches aplicados a `spec.md` con los casos borde `CB-006` y `CB-007` |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | `plan.md` redactado con 6 decisiones `DEC-001` a `DEC-006`, 6 contratos, estrategia de testing y matriz de cobertura de 17 filas |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` redactado con 13 tareas atómicas, dependencias acíclicas y cobertura de 5 requisitos funcionales, 5 no funcionales y 7 casos borde |
| 2026-11-14 | T4 | `tasked` | `implementing` | `planner` | G2 verificada por el orquestador, trece tareas cerradas con evidencia y `--all` con código 0 |
| 2026-11-14 | T5 | `implementing` | `implemented` | `planner` | G3 verificada en el commit `cf9caf5` con trece tareas cerradas, 167 pruebas de la suite del mecanismo y 48 de las herramientas de Git en verde |
| 2026-11-14 | T6 | `implemented` | `validated` | `planner` | G4 firmada en el commit `f070cbf`, dictamen `CONVERGIDO` de 17 de 17 filas e integración `b018ab8` con dos padres y rama eliminada |
| 2026-11-14 | T7 | `validated` | `released` | `planner` | release v0.7.0 publicado con tag anotado `v0.7.0` verificado sobre el commit de empaquetado y G6 firmada |
