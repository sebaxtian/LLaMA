---
id: SPEC-013
title: Cierre de la reauditoría de conformidad
status: implemented
version: 0.6.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/reauditoria-cierre
release: ""
supersedes: ""
superseded_by: ""
---

# Cierre de la reauditoría de conformidad

## Contexto y objetivo

La reauditoría de cierre registrada en `docs/sdd/auditoria_cierre_v0_7_0.md` evaluó la base normativa v2, las doce specs, el validador, la suite, la matriz de agentes, el flujo de integración continua y el historial de integración sobre el commit `5efac03`. La reauditoría cerró los cuarenta y un hallazgos de `docs/sdd/auditoria_cumplimiento_sdd.md` con evidencia o con exención registrada, dejó AUD-071 en estado parcial y añadió dieciséis observaciones nuevas: dos de severidad Alta, ocho de severidad Media y seis de severidad Baja. El veredicto global fue `NO CONFORME`, sostenido por dos dimensiones no conformes: D8 por AUD-073, porque el flujo de integración continua no prepara el árbol que declara verificar y su resultado no condiciona la integración, y D9 por AUD-085, porque la comprobación de sincronización de release exige una salida imposible de obtener cuando `dev` contiene trabajo no publicado.

Objetivo: fijar el contrato que cierra las dieciséis observaciones de la reauditoría de cierre, de modo que cada observación quede cerrada con artefacto y evidencia verificable y la reauditoría posterior emita veredicto global `CONFORME`.

Resultado esperado: flujo de integración continua que prepara el árbol con `actions/checkout`, instala Python con `actions/setup-python`, ejecuta el validador y la suite en cada Pull Request y expone el check `verify` del flujo `SDD` como exigible en las reglas de protección de `main` y de `dev`; comprobación de sincronización expresada como relación de ancestría verificable; gramática de ramas que admite `docs/`; dos ventanas de legado declaradas por escrito con su motivo y su límite; matriz de permisos del orquestador sin contradicción y sin escritura de artefactos; reportes de `SPEC-008` a `SPEC-011` con su cierre de integración declarado; atribución corregida de la escritura de transiciones; y consistencia documental de las guías, el flujo Git, `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md`.

La feature no reabre requisito alguno de `SPEC-008` a `SPEC-012` ni cambia el estado de esas cinco specs. Las correcciones de la base normativa se limitan a las afirmaciones señaladas por la reauditoría y no alteran el orden de precedencia ni el rango de documento alguno. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen ni la autorización de un release.

### Trazabilidad con el informe de reauditoría

| Observación | Severidad | Requisito | Criterio de aceptación |
|---|---|---|---|
| `AUD-008` | Baja | `RF-001` | `CA-001` |
| `AUD-015` | Baja | `RF-002` | `CA-002` |
| `AUD-024` | Media | `RF-003` | `CA-003` |
| `AUD-036` | Media | `RF-004` | `CA-004` |
| `AUD-037` | Media | `RF-005` | `CA-005` |
| `AUD-045` | Media | `RF-006` | `CA-006` |
| `AUD-046` | Media | `RF-007` | `CA-007` |
| `AUD-056` | Media | `RF-008` | `CA-008` |
| `AUD-065` | Media | `RF-009` | `CA-009` |
| `AUD-073` | Alta | `RF-010` | `CA-010` |
| `AUD-074` | Baja | `RF-011` | `CA-011` |
| `AUD-085` | Alta | `RF-012` | `CA-012` |
| `AUD-086` | Media | `RF-013` | `CA-013` |
| `AUD-095` | Baja | `RF-014` | `CA-014` |
| `AUD-096` | Baja | `RF-015` | `CA-014` |
| `AUD-097` | Baja | `RF-016` | `CA-014` |

Cada una de las dieciséis observaciones queda cubierta por un requisito funcional y por al menos un criterio de aceptación. Los requisitos no funcionales y los casos borde completan las condiciones de cierre de la reauditoría posterior y no responden a una observación aislada.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`, autoriza la corrección de la sección protegida de `SPEC-010` y `SPEC-011` y delega por escrito la escritura de los documentos de raíz cuando corresponde; no delega la firma.
- **Orquestador (`sdd`):** ejecuta el validador y la suite, verifica G2, G3 y G5, registra el resultado de cada verificación, ejecuta `git add` y `git commit` de los artefactos de control y no redacta artefactos ni escribe bajo `specs/`; no declara aprobación alguna.
- **Agente `planner`:** redacta los artefactos de esta spec dentro de `specs/013-cierre-reauditoria-conformidad/`, escribe las transiciones T4, T5, T6 y T7 sobre la verificación registrada por el orquestador y no escribe fuera de `specs/`; no declara compuertas.
- **Agente `coder`:** escribe en `src/`, `tests/`, `tools/` y `.github/` la preparación del árbol, las comprobaciones nuevas y sus pruebas, y cierra tareas en `tasks.md` con la evidencia transcrita.
- **Agente `documenter`:** redacta las correcciones de `docs/`, `AGENTS.md`, `MEMORY.md` y `CHANGELOG.md` dentro del alcance declarado y como delegado explícito del propietario para los documentos de raíz.
- **Agente `reviewer`:** escribe el reporte de validación de esta spec con la matriz de trazabilidad y el dictamen; no modifica código ni documentos normativos y no declara G4.
- **Agente `auditor`:** ejecuta la reauditoría posterior, registra el veredicto por dimensión y no edita requisitos ni declara compuertas.

## Requisitos funcionales (EARS)

### RF-001

`El sistema DEBE alinear las guías `docs/sdd/guia_spec_md.md`, `docs/sdd/guia_clarify_md.md` y `docs/sdd/referencia_7_etapas_sdd.md` con las plantillas de rango 5, DEBE declarar en el encabezado de cada guía del corpus su carácter no normativo y el rango «Sin rango», y DEBE sustituir la denominación «Definition of Done» por «criterio de aceptación».`

### RF-002

`El sistema DEBE declarar en la definición del rol orquestador una tabla de 7 etapas numeradas de 1 a 7 —1 Specify, 2 Clarify, 3 Plan, 4 Tasks, 5 Implement, 6 Validate y 7 Release—, DEBE numerar la primera etapa como 1 Specify y la séptima como 7 Release, y NO DEBE conservar una tabla de 6 etapas ni una numeración que comience en 2 u omita Release.`

### RF-003

`El sistema DEBE retirar la tercera casilla de la compuerta G4 de la sección de aprobaciones de `SPEC-010` y de `SPEC-011`, DEBE conservar 2 casillas —G1 y G4— en cada sección de aprobaciones, y DEBE registrar un error cuando una sección de aprobaciones declare más de 1 casilla para una misma compuerta, con independencia de que la casilla adicional esté marcada o sin marcar.`

### RF-004

`El sistema DEBE declarar en el contrato del validador del protocolo operativo y en `AGENTS.md` que el validador verifica la firma criptográfica del commit de aprobación y la pertenencia de la clave firmante a `docs/sdd/firmantes_autorizados`, y NO DEBE conservar afirmación que declare esas verificaciones no realizadas.`

### RF-005

`El sistema DEBE declarar en el contrato del validador 2 ventanas de legado con su motivo y su límite: una ventana estructural para `SPEC-001` a `SPEC-009`, que alcanza las comprobaciones C-01 a C-13, y una ventana de trazabilidad para `SPEC-008` a `SPEC-011`, que alcanza las comprobaciones C-14 a C-18, y NO DEBE ampliar ninguna de las 2 ventanas sin una spec posterior.`

### RF-006

`El sistema DEBE declarar en el reporte de validación de `SPEC-008`, `SPEC-009`, `SPEC-010` y `SPEC-011` una sección `## Cierre de integración` con la línea `Merge:` que transcribe el identificador del merge de integración y la línea `Release:` vacía, DEBE conservar el estado `validated` de las 4 specs con su matriz y su dictamen sin alteración, y NO DEBE reabrir requisito alguno de esas specs.`

Valores fijados del cierre de integración:

| Spec | `Merge:` | `Release:` |
|---|---|---|
| `SPEC-008` | `49caac9` | vacía |
| `SPEC-009` | `09eaf34` | vacía |
| `SPEC-010` | `94c2ea1` | vacía |
| `SPEC-011` | `9df8446` | vacía |

### RF-007

`CUANDO se ejecuta la comprobación de la referencia a la spec en los commits, el sistema DEBE acotar su alcance a los commits posteriores al último tag anotado de release o, en su defecto, a los commits posteriores al ancestro común con `main`, DEBE excluir los merges del alcance, DEBE examinar al menos 1 commit cuando el rango no esté vacío, DEBE examinar al menos 1 commit sobre `dev` cuando exista al menos 1 commit de implementación posterior al último tag anotado de release, DEBE informar la comprobación como no aplicable cuando el alcance resulte vacío, y DEBE registrar un error por cada commit de implementación del alcance sin la cadena `Spec: SPEC-NNN`.`

### RF-008

`El sistema DEBE declarar en la tabla de escritura de estados del protocolo que el rol `planner` escribe las transiciones T4, T5, T6 y T7 sobre la verificación registrada por el orquestador, DEBE conservar la fecha, la evidencia y la secuencia de estados de las filas T4, T5 y T6 del historial de `SPEC-012`, que quedan conformes, NO DEBE editar esas filas y NO DEBE alterar el estado vigente de la spec.`

### RF-009

`El sistema DEBE declarar en el protocolo y en la definición del rol orquestador que el orquestador verifica compuertas, ejecuta el validador y ejecuta `git add` y `git commit` de los artefactos de control sin redactar artefacto alguno, DEBE reducir a 0 sus atribuciones de escritura sobre `specs/`, DEBE retirar de `.opencode/agents/sdd.md` la concesión de escritura sobre `specs/`, DEBE conservar la prohibición de escribir la sección de aprobaciones, y NO DEBE mantener contradicción entre la matriz de permisos y el cuerpo del rol.`

### RF-010

`El sistema DEBE preparar el árbol del repositorio con `actions/checkout` y el entorno de Python con `actions/setup-python` en el flujo `SDD` de `.github/`, DEBE ejecutar en ese flujo el validador y la suite de pruebas en cada Pull Request dirigido a `main` y a `dev`, DEBE nombrar el job `verify` y DEBE declarar exigible el check `verify` del flujo `SDD` en las reglas de protección de las 2 ramas, con la exigibilidad documentada en `docs/Flujo_de_Trabajo_Git.md` y aplicada con la herramienta de protección existente.`

### RF-011

`El sistema DEBE corregir en `docs/Flujo_de_Trabajo_Git.md` la afirmación sobre la ausencia de suite automatizada para la raíz y DEBE declarar la suite del mecanismo de control, sus 131 pruebas y su ejecución en el job `verify` del flujo `SDD`, de modo que el número de afirmaciones que nieguen su existencia sea 0.`

### RF-012

`El sistema DEBE expresar la comprobación de sincronización previa al release como la relación de ancestría que exige que `main` sea ancestro de `dev` y que el tag del release apunte a un commit alcanzable desde `main`, NO DEBE conservar la exigencia de un conteo simétrico entre las 2 ramas y NO DEBE tratar como bloqueo el estado `48 0` de `dev` respecto de `main` cuando la ancestría se cumple.`

### RF-013

`El sistema DEBE admitir en la gramática de nombres de rama los prefijos `feat/`, `fix/`, `hotfix/`, `docs/` y `release/vX-Y-Z`, DEBE admitir `docs/` para los cambios exclusivamente documentales con la misma validación de minúsculas, números y guiones y la misma longitud de nombre de 3 a 63 caracteres que los demás prefijos, y DEBE rechazar los prefijos fuera de esa lista de 5.`

### RF-014

`El sistema DEBE actualizar en `MEMORY.md` el estado de las specs para que coincida con `specs/INDEX.md` y con el frontmatter de cada spec, con 0 divergencias de estado entre los 3 soportes.`

### RF-015

`El sistema DEBE registrar en la tabla de inventario de `docs/sdd/README.md` una fila para el informe `docs/sdd/auditoria_cierre_v0_7_0.md`, con su ruta y su carácter de evidencia no normativa, y DEBE dejar en 0 el número de archivos del corpus sin fila en esa tabla.`

### RF-016

`El sistema DEBE completar en `CHANGELOG.md` el historial de releases con los 8 tags anotados publicados de `v0.1.0` a `v0.6.0`, que alcanzan hasta el release anterior a `v0.7.0`, y DEBE registrar en cada fila la versión, la fecha y el tag, de modo que el número de releases publicados sin fila sea 0.`

## Requisitos no funcionales

### RNF-001

`La reauditoría posterior DEBE emitir veredicto global «CONFORME» con 0 observaciones abiertas de las 16 registradas y 10 de 10 dimensiones sin observación vigente.`

### RNF-002

`La validación agregada del corpus DEBE completar en 300 segundos o menos sobre el commit validado.`

### RNF-003

`Dos ejecuciones del validador sobre el mismo commit DEBEN producir 0 diferencias en el conjunto de hallazgos.`

### RNF-004

`Cada comprobación nueva DEBE declarar al menos 1 prueba positiva y 1 prueba negativa en la suite del mecanismo de control.`

### RNF-005

`Las correcciones de esta spec DEBEN conservar sin cambios el 100 % de los requisitos, los criterios de aceptación y el estado de `SPEC-008`, `SPEC-009`, `SPEC-010`, `SPEC-011` y `SPEC-012`.`

### RNF-006

`La verificación DEBE ejecutarse sin acceso a red, servicio externo ni credencial, y DEBE conservar los 3 códigos de salida: 0 sin hallazgos, 1 con error de validación y 2 ante error de uso del comando.`

### RNF-007

`El número de contradicciones entre documentos de rango 2, rango 3 y rango 4 sobre las afirmaciones corregidas DEBE ser 0 tras la implementación.`

### RNF-008

`Cada documento corregido DEBE conservar su rango y su carácter declarados en el encabezado, con 100 % de los documentos de la base con declaración vigente.`

## Casos borde

### CB-001

`SI la gramática de ramas recibe un nombre con prefijo `docs/` que contiene una mayúscula, un guion bajo o un carácter especial, ENTONCES el sistema DEBE rechazar el nombre y DEBE informar el prefijo admitido.`

### CB-002

`SI un nombre con prefijo `docs/` tiene menos de 3 caracteres o más de 63 caracteres de nombre, ENTONCES el sistema DEBE rechazar el nombre y DEBE informar el rango de longitud admitido.`

### CB-003

`SI `main` no es ancestro de `dev` al preparar el release, ENTONCES el sistema DEBE detener el empaquetado y DEBE informar la relación de ancestría incumplida.`

### CB-004

`SI el tag del release apunta a un commit no alcanzable desde `main`, ENTONCES el sistema DEBE detener el release y NO DEBE declarar la sincronización cumplida.`

### CB-005

`SI el alcance de la comprobación de la referencia a la spec resulta vacío por ausencia de tag anotado de release y de ancestro común con `main`, o por ausencia de commits de implementación posteriores al punto de corte, ENTONCES el sistema DEBE informar la comprobación como no aplicable y NO DEBE producir error por esa causa.`

### CB-006

`SI la sección de aprobaciones declara una tercera casilla de G4 sin marcar, ENTONCES la validación DEBE registrar un error de ubicación única con el identificador de la spec.`

### CB-007

`SI el reporte de `SPEC-008`, `SPEC-009`, `SPEC-010` o `SPEC-011` declara un dictamen no convergido, ENTONCES el registro del merge y de la línea de release vacía DEBE añadirse sin alterar la matriz ni el dictamen.`

### CB-008

`SI una spec en estado `validated` declara un tag de release en su reporte, ENTONCES la validación DEBE registrar un error por release declarado sin publicación.`

### CB-009

`SI el flujo de integración continua se ejecuta sin `actions/checkout`, ENTONCES la ejecución DEBE fallar por ausencia de los archivos que valida y NO DEBE declarar la verificación cumplida.`

### CB-010

`SI las reglas de protección de `main` o de `dev` no declaran exigible el check `verify` del flujo `SDD`, ENTONCES la verificación de G5 DEBE quedar bloqueada y DEBE registrar la ausencia del check exigible.`

### CB-011

`SI una spec fuera de la ventana de legado que le corresponde incumple una de las comprobaciones C-01 a C-13 o C-14 a C-18, ENTONCES la validación DEBE registrar un error y NO DEBE degradarlo a advertencia.`

### CB-012

`SI una guía del corpus ya declara su rango y su carácter y no conserva identificadores fuera de formato, ENTONCES la corrección NO DEBE modificar la guía y DEBE dejar constancia de su conformidad previa.`

### CB-013

`SI `MEMORY.md`, `docs/sdd/README.md` o `CHANGELOG.md` conserva una divergencia con `specs/INDEX.md` o con el historial de tags, ENTONCES la validación DEBE registrar un error con el documento y el valor en conflicto.`

### CB-014

`SI el orquestador intenta escribir un artefacto bajo `specs/`, ENTONCES el sistema DEBE denegar la escritura y la transición DEBE quedar atribuida al rol que `tasks.md` declara para esa tarea.`

### CB-015

`SI una observación de la reauditoría exige cambiar un requisito de una spec publicada, ENTONCES la corrección DEBE detenerse para esa observación y el cambio DEBE tramitarse por una spec nueva.`

### CB-016

`SI el orquestador no ha registrado la verificación de la compuerta que habilita una transición de T4 a T7, ENTONCES el `planner` NO DEBE escribir la transición y DEBE informar la verificación ausente.`

## Fuera de alcance

- El release `v0.7.0`, su empaquetado, su tag y su compuerta G6: se ejecutan después de esta spec y la citan como antecedente.
- El cambio del contenido funcional de `SPEC-008`, `SPEC-009`, `SPEC-010`, `SPEC-011` y `SPEC-012`: esta spec corrige registros de cierre, atribuciones de historial y casillas residuales, no requisitos ni criterios.
- La reapertura de una spec publicada o el cambio del estado de `SPEC-008` a `SPEC-012`.
- La reescritura de `docs/sdd/auditoria_cumplimiento_sdd.md` y de `docs/sdd/auditoria_cierre_v0_7_0.md`: ambos se citan como evidencia y no se modifican.
- La modificación del orden de precedencia, del rango de documento o de la constitución.
- La ampliación del alcance del validador a la veracidad de la evidencia transcrita o a la ejecución real de los scripts `.bat`.
- La verificación de la configuración remota de protección por una vía distinta de la declaración de las reglas del repositorio.
- Hardware, modelos, cuantizaciones y benchmarks de ejecución local.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.

## Criterios de aceptación

### CA-001

`DADAS las guías del corpus, CUANDO se contrastan con las plantillas de rango 5, ENTONCES cada guía declara en el encabezado su carácter no normativo y el rango «Sin rango», no conserva identificadores de ejemplo con menos de tres dígitos ni la denominación «Definition of Done», y una guía ya conforme queda sin modificación con constancia de su conformidad previa.`

Cubre: `RF-001`, `CB-012`.

### CA-002

`DADA la definición del rol orquestador, CUANDO se contrasta su tabla de etapas con el ciclo del protocolo, ENTONCES la tabla declara 7 etapas numeradas de 1 a 7, con 1 Specify como primera fila y 7 Release como última, y no conserva una tabla de 6 etapas ni una numeración que comience en 2 u omita Release.`

Cubre: `RF-002`.

### CA-003

`DADAS las secciones de aprobaciones de `SPEC-010` y `SPEC-011`, CUANDO se ejecuta la validación, ENTONCES cada una declara 2 casillas y ninguna más, y una sección con una tercera casilla de G4 marcada o sin marcar produce un error de ubicación única.`

Cubre: `RF-003`, `CB-006`.

### CA-004

`DADOS el contrato del validador del protocolo y `AGENTS.md`, CUANDO se contrastan con las comprobaciones ejecutadas, ENTONCES ambos declaran que el validador verifica la firma criptográfica del commit de aprobación y la pertenencia de la clave firmante a `docs/sdd/firmantes_autorizados`, y no conservan afirmación que declare esas verificaciones no realizadas.`

Cubre: `RF-004`.

### CA-005

`DADAS las specs `SPEC-001` a `SPEC-011`, CUANDO se ejecuta la validación, ENTONCES el contrato del validador declara 2 ventanas de legado, cada una con su conjunto de specs, su conjunto de comprobaciones, su motivo y su límite, una spec fuera de su ventana produce un error y una spec dentro de su ventana produce una advertencia.`

Cubre: `RF-005`, `CB-011`.

### CA-006

`DADOS los reportes de `SPEC-008` a `SPEC-011`, CUANDO se ejecuta la validación, ENTONCES cada reporte declara la sección `## Cierre de integración` con la línea `Merge:` propia y la línea `Release:` vacía, las 4 specs conservan el estado `validated` y su matriz y su dictamen intactos, un tag declarado en estado `validated` produce un error y un dictamen no convergido se conserva sin alteración.`

Cubre: `RF-006`, `CB-007`, `CB-008`.

### CA-007

`DADO un historial con tag anotado de release, CUANDO se ejecuta la comprobación de la referencia a la spec, ENTONCES el alcance son los commits posteriores a ese tag, con los merges excluidos y con al menos 1 commit examinado cuando el rango no está vacío; sin tag el alcance son los commits posteriores al ancestro común con `main`; sobre `dev` se examina al menos 1 commit cuando existe al menos 1 commit de implementación posterior al último tag; y un alcance vacío se informa como no aplicable.`

Cubre: `RF-007`, `CB-005`.

### CA-008

`DADO el historial de transiciones de `SPEC-012` y la tabla de escritura de estados del protocolo, CUANDO se contrastan entre sí, ENTONCES la tabla atribuye a `planner` la escritura de T4, T5, T6 y T7 sobre la verificación registrada por el orquestador, las filas T4, T5 y T6 conservan fecha, evidencia y secuencia sin edición, el estado vigente de la spec no cambia y una transición sin verificación registrada no se escribe.`

Cubre: `RF-008`, `CB-016`.

### CA-009

`DADOS el protocolo y la definición del rol orquestador, CUANDO se contrastan la matriz de permisos y el cuerpo del rol, ENTONCES el orquestador verifica compuertas y registra resultados, ejecuta el validador y `git add` y `git commit` de los artefactos de control, no redacta artefacto alguno, sus atribuciones de escritura sobre `specs/` son 0, la prohibición de escribir la sección de aprobaciones se conserva, `.opencode/agents/sdd.md` no concede escritura sobre `specs/` y una escritura intentada bajo `specs/` queda denegada.`

Cubre: `RF-009`, `CB-014`.

### CA-010

`DADO un Pull Request dirigido a `main` o a `dev`, CUANDO se ejecuta el flujo `SDD` de integración continua, ENTONCES prepara el árbol con `actions/checkout`, instala Python con `actions/setup-python`, ejecuta el validador y la suite, el job se llama `verify`, el check `verify` figura como exigible en las reglas de protección de las 2 ramas con la exigibilidad documentada en `docs/Flujo_de_Trabajo_Git.md`, una ejecución sin `actions/checkout` falla y la ausencia del check exigible bloquea G5.`

Cubre: `RF-010`, `CB-009`, `CB-010`.

### CA-011

`DADO `docs/Flujo_de_Trabajo_Git.md`, CUANDO se contrasta con la suite del mecanismo de control, ENTONCES declara su existencia, sus 131 pruebas y su ejecución en el job `verify` del flujo `SDD`, y no conserva afirmación que niegue su existencia.`

Cubre: `RF-011`.

### CA-012

`DADAS las ramas `main` y `dev` y el tag del release, CUANDO se prepara el empaquetado, ENTONCES la comprobación exige que `main` sea ancestro de `dev` y que el tag apunte a un commit alcanzable desde `main`, no conserva la exigencia de conteo simétrico, no trata como bloqueo el estado `48 0` de `dev` respecto de `main` cuando la ancestría se cumple, la falta de ancestría detiene el empaquetado y un tag no alcanzable detiene el release.`

Cubre: `RF-012`, `CB-003`, `CB-004`.

### CA-013

`DADA la gramática de nombres de rama, CUANDO se valida un nombre, ENTONCES `docs/` se admite con las mismas reglas de minúsculas, números y guiones y con la misma longitud de 3 a 63 caracteres, la lista admitida es `feat/`, `fix/`, `hotfix/`, `docs/` y `release/vX-Y-Z`, y un prefijo fuera de esa lista de 5 se rechaza.`

Cubre: `RF-013`, `CB-001`, `CB-002`.

### CA-014

`DADOS `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md`, CUANDO se contrastan con `specs/INDEX.md` y con los tags publicados, ENTONCES los estados coinciden con 0 divergencias, la tabla de inventario registra el informe de reauditoría con 0 archivos sin fila, el historial de releases registra los 8 tags de `v0.1.0` a `v0.6.0` hasta el release anterior a `v0.7.0` con 0 releases publicados sin fila, y una divergencia restante produce un error.`

Cubre: `RF-014`, `RF-015`, `RF-016`, `CB-013`.

### CA-015

`DADAS las 16 observaciones cerradas, CUANDO se ejecuta la reauditoría posterior, ENTONCES emite veredicto global «CONFORME» con 0 observaciones abiertas y 10 de 10 dimensiones sin observación vigente.`

Cubre: `RNF-001`.

### CA-016

`DADO el corpus en el commit validado, CUANDO se ejecuta la validación agregada en 2 ocasiones y se inspecciona la suite, ENTONCES cada ejecución completa en 300 segundos o menos, las 2 salidas presentan 0 diferencias en el conjunto de hallazgos, cada comprobación nueva declara al menos 1 prueba positiva y 1 prueba negativa, y la ejecución no requiere red, servicio externo ni credencial y conserva los códigos de salida 0, 1 y 2.`

Cubre: `RNF-002`, `RNF-003`, `RNF-004`, `RNF-006`.

### CA-017

`DADAS `SPEC-008` a `SPEC-012`, CUANDO se contrastan con su versión anterior, ENTONCES el 100 % de sus requisitos, criterios de aceptación y estados queda sin cambios, y una observación que exija cambiar un requisito de una spec publicada detiene la corrección y se tramita por una spec nueva.`

Cubre: `RNF-005`, `CB-015`.

### CA-018

`DADOS los documentos de rango 2, rango 3 y rango 4 corregidos, CUANDO se contrastan entre sí, ENTONCES el número de contradicciones sobre las afirmaciones corregidas es 0 y el 100 % de los documentos corregidos conserva su rango y su carácter en el encabezado.`

Cubre: `RNF-007`, `RNF-008`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [ ] G4: `- Approved by: Agent Sebaxtian` (YYYY-MM-DD)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación cerrada: 12 ambigüedades resueltas, caso borde `CB-016` añadido y parches aplicados a requisitos, casos borde y criterios |
| 0.3.0 | 2026-11-14 | Plan: arquitectura de doce componentes, contratos del flujo, de las reglas de protección, de la sincronización, de la gramática, de las comprobaciones C-09, C-13, C-16 y C-17, de las dos ventanas de legado y de las correcciones documentales, once decisiones técnicas y matriz de cobertura de dieciséis requisitos, ocho no funcionales y dieciséis casos borde |
| 0.4.0 | 2026-11-14 | Tasks: descomposición en cuarenta y cuatro tareas atómicas con cobertura de dieciséis requisitos funcionales, ocho no funcionales y dieciséis casos borde, dependencias acíclicas, estimaciones entre 15 y 30 minutos y una tarea reservada al propietario por la sección protegida |
| 0.5.0 | 2026-11-14 | Implementación del cierre de la reauditoría |
| 0.6.0 | 2026-11-14 | Cierre de la implementación y verificación G3 |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con dieciséis requisitos funcionales, ocho no funcionales, quince casos borde y dieciocho criterios de aceptación |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con 12 hallazgos resueltos y sin casillas pendientes, y parches aplicados a `spec.md` |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | línea de G1 firmada en `spec.md` en el commit `c61432d` y `plan.md` escrito con once decisiones y la matriz de cobertura de dieciséis requisitos, ocho no funcionales y dieciséis casos borde |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` escrito con cuarenta y cuatro tareas atómicas, cobertura de dieciséis requisitos funcionales, ocho no funcionales y dieciséis casos borde, dependencias acíclicas y estimaciones entre 15 y 30 minutos |
| 2026-11-14 | T4 | `tasked` | `implementing` | `planner` | verificación de G2 registrada por el orquestador, cuarenta y tres tareas cerradas con evidencia y `--all` con código 0 |
| 2026-11-14 | T5 | `implementing` | `implemented` | `planner` | G3 verificada en el commit `80e589b` con cuarenta y cuatro tareas cerradas, 156 pruebas en verde y `--all` con código 0 |
