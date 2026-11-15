---
id: SPEC-011
title: Práctica operativa SDD verificable
status: released
version: 0.6.0
created: 2026-11-14
updated: 2026-11-14
owner: Agent Sebaxtian
branch: feat/practica-operativa-sdd
release: "v0.7.0"
supersedes: ""
superseded_by: ""
---

# Práctica operativa SDD verificable

## Contexto y objetivo

El informe `docs/sdd/auditoria_cumplimiento_sdd.md` concentra en el bloque B3 los defectos de la práctica operativa. Los roles `coder`, `planner` y `reviewer` no declaran reglas de shell, de modo que el menor privilegio no es verificable (`AUD-061`). No existe rol de auditoría en `.opencode/` y la función se ejecutó con los permisos del rol de documentación (`AUD-063`). La configuración no declara la precedencia entre permisos solapados y el permiso efectivo depende del orden de resolución del cliente (`AUD-064`). No existe integración continua ni hook, y la suite de pruebas no se ejecuta en la integración (`AUD-071`). Cuatro hallazgos de la práctica Git y uno del contexto operativo se corrigieron en la operación y quedaron sin registro de cierre: la rama de integración sin el commit publicado (`AUD-081`), la referencia remota obsoleta del release anterior (`AUD-082`), la rama sin decisión archivada (`AUD-083`), los seis documentos fuera de commit (`AUD-084`) y los hechos obsoletos de `MEMORY.md` (`AUD-091`).

Objetivo: fijar el contrato de la práctica operativa verificable que cierra los nueve hallazgos del bloque B3, de modo que cada rol declare su matriz de permisos con precedencia explícita, el rol de auditoría exista con escritura limitada a su informe, la integración continua ejecute la verificación en cada Pull Request sin efectos remotos y cada corrección de la práctica Git quede registrada como cerrada con la evidencia que la acredita.

Resultado esperado: seis roles con permisos de lectura y de escritura por ruta, reglas de shell y política de subagentes; tres reglas de precedencia declaradas y aplicadas; rol `auditor` con lectura completa y escritura única en el informe de auditoría; `reviewer` sin subagentes ni escritura de código o configuración; `coder` acotado a tres raíces y al cierre de tareas; flujo de integración continua que ejecuta la validación agregada y la suite por Pull Request y falla si cualquiera devuelve error, sin push, tag ni operación sobre el remoto; nueve hallazgos registrados como cerrados con evidencia; y una prueba de configuración no destructiva que contrasta los permisos declarados.

La feature se redacta con la base v2 vigente. No modifica `docs/constitution.md`, el protocolo operativo, el flujo Git ni las plantillas; en `AGENTS.md` solo alinea el mapa de agentes con los seis roles que la constitución declara, y en `MEMORY.md` actualiza la lista de agentes y la mención de la integración continua. No implementa el bloque B4 del informe y no reescribe las specs publicadas. Las raíces `src/`, `tests/` y `tools/` se citan como límites de permiso y no como rutas de implementación. Un resultado favorable del validador acredita la estructura y la coherencia del contrato, no la firma del commit de aprobación ni la conformidad del régimen.

### Trazabilidad con el informe de auditoría

| Hallazgo | Requisitos que lo resuelven | Criterios de aceptación |
|---|---|---|
| `AUD-061` | `RF-001`, `RF-002`, `RF-004`, `RF-005` | `CA-001`, `CA-002`, `CA-005`, `CA-006` |
| `AUD-063` | `RF-003`, `RNF-005` | `CA-003`, `CA-004` |
| `AUD-064` | `RF-002`, `RF-011`, `RNF-004` | `CA-002`, `CA-013` |
| `AUD-071` | `RF-006`, `RF-007`, `RNF-001`, `RNF-002` | `CA-007`, `CA-008` |
| `AUD-081` | `RF-008` | `CA-009` |
| `AUD-082` | `RF-008` | `CA-009` |
| `AUD-083` | `RF-008` | `CA-010` |
| `AUD-084` | `RF-008` | `CA-010` |
| `AUD-091` | `RF-009` | `CA-011` |

`RF-010` no responde a un hallazgo del informe: desarrolla el contraste exigido por el objetivo de la spec y se verifica en `CA-012`. `RF-012` y `RF-013` alinean la documentación operativa con los seis roles de la constitución y con la integración continua, no responden a un hallazgo del informe y se verifican en `CA-016` y `CA-017`.

## Actores y permisos

- **Propietario (`Agent Sebaxtian`):** declara G1 y G4 mediante un commit firmado con una clave de `docs/sdd/firmantes_autorizados`; no delega la firma y no acepta una aprobación emitida por un agente.
- **Orquestador (`sdd`):** verifica G2, G3 y G5, ejecuta el validador, lanza subagentes y escribe las transiciones `implementing`, `implemented` y `validated`; no declara aprobaciones y no escribe la sección protegida.
- **Agente `planner`:** redacta `spec.md`, `clarify.md`, `plan.md` y `tasks.md` dentro de `specs/`; no escribe código, configuración de agentes ni la sección de aprobaciones.
- **Agente `documenter`:** escribe `docs/`, `AGENTS.md` y la documentación de referencia; no modifica requisitos de una spec aprobada.
- **Agente `coder`:** escribe en `src/`, `tests/` y `tools/` y cierra tareas en `tasks.md`; no escribe fuera de esas raíces ni en `.opencode/`.
- **Agente `reviewer`:** escribe el reporte de validación de la spec en curso; no lanza subagentes, no modifica código ni configuración y no declara G4.
- **Agente `auditor`:** se declara como subagente con lectura de la base normativa completa y de las specs, shell de solo lectura y subagentes denegados; escribe solo informes de auditoría bajo `docs/sdd/auditoria_*.md`; no modifica requisitos, código, configuración ni base normativa, y no aprueba compuertas.
- **Integración continua:** ejecuta la validación agregada del corpus y la suite de pruebas en cada Pull Request dirigido a `dev` o a `main`, en un entorno Windows con Python 3.12; no ejecuta push, creación de tag ni operación sobre el remoto.

## Requisitos funcionales (EARS)

### RF-001

`El sistema DEBE declarar, para cada uno de los seis roles de agente, los permisos de lectura y de escritura por ruta, la allowlist de comandos de shell y la política de subagentes en el archivo del rol dentro de `.opencode/agents/`.`

### RF-002

`El sistema DEBE resolver los permisos solapados con cuatro reglas declaradas en la configuración de agentes: la denegación explícita prevalece sobre cualquier concesión, la ruta más específica prevalece sobre la más general, la ruta no declarada está denegada y una concesión de escritura no autoriza a declarar compuertas.`

### RF-003

`El sistema DEBE declarar el rol `auditor` como subagente con lectura sobre la base normativa y las specs, shell de solo lectura, subagentes denegados, sin permiso de modificar requisitos, código, configuración ni base normativa, y con escritura limitada a los informes de auditoría `docs/sdd/auditoria_*.md`.`

### RF-004

`La configuración del rol `reviewer` NO DEBE admitir el lanzamiento de subagentes ni la escritura en rutas de código o de configuración, y su escritura DEBE limitarse al reporte de validación de la spec en curso.`

### RF-005

`La configuración del rol `coder` NO DEBE admitir escritura fuera de `src/`, `tests/` y `tools/`, y su única escritura fuera de esas tres raíces DEBE ser el cierre de tareas en `tasks.md`.`

### RF-006

`CUANDO se abre, se reabre o se actualiza un Pull Request dirigido a `dev` o a `main`, el sistema DEBE ejecutar la validación agregada del corpus de specs y la suite de pruebas del mecanismo de control, y DEBE finalizar en fallo si cualquiera de las dos devuelve un código de salida distinto de cero.`

### RF-007

`El flujo de integración continua NO DEBE ejecutar push, creación de tag ni operación sobre el remoto.`

### RF-008

`CUANDO se cierra el alcance de esta spec, el sistema DEBE verificar los hallazgos `AUD-081`, `AUD-082`, `AUD-083` y `AUD-084` y DEBE registrar cada uno en el reporte de validación como cerrado con la evidencia que lo acredita.`

### RF-009

`CUANDO se cierra el alcance de esta spec, el sistema DEBE verificar el hallazgo `AUD-091` contra el estado de `MEMORY.md` y DEBE registrar su cierre en el reporte de validación con la evidencia que lo acredita.`

### RF-010

`El sistema DEBE contrastar los permisos declarados por rol con una prueba de configuración no destructiva que informe, por rol, las rutas concedidas y las rutas denegadas.`

### RF-011

`El sistema DEBE declarar en `opencode.jsonc` el orden de precedencia de los permisos globales, DEBE hacerlo coincidir con las cuatro reglas de rol de `RF-002` y NO DEBE admitir que una concesión global amplíe una denegación de rol.`

### RF-012

`CUANDO se implementa esta spec, el sistema DEBE añadir el rol `auditor` al mapa de agentes de `AGENTS.md` y DEBE conservar su longitud entre 30 y 70 líneas útiles, sin alterar regla alguna de la base normativa.`

### RF-013

`CUANDO se implementa esta spec, el sistema DEBE actualizar en `MEMORY.md` la lista de agentes y la mención de la integración continua, y NO DEBE conservar un hecho operativo que contradiga el estado del repositorio.`

## Requisitos no funcionales

### RNF-001

`La ejecución conjunta de la validación agregada y de la suite de pruebas en la integración continua DEBE completar en 300 segundos o menos por Pull Request.`

### RNF-002

`La integración continua NO DEBE requerir credenciales ni secretos del repositorio para ejecutarse.`

### RNF-003

`La prueba de configuración DEBE completarse en 60 segundos o menos y NO DEBE modificar archivos versionados.`

### RNF-004

`La configuración de agentes DEBE declarar cero rutas con concesión y denegación simultáneas de la misma especificidad.`

### RNF-005

`El rol `auditor` DEBE residir en una sola ruta de `.opencode/agents/` y su declaración NO DEBE duplicarse en otro rol.`

### RNF-006

`La configuración de permisos NO DEBE contener credenciales ni secretos del repositorio.`

### RNF-007

`La integración continua DEBE ejecutarse en un entorno Windows con Python 3.12 y NO DEBE requerir servicios externos.`

### RNF-008

`La suite de pruebas DEBE completar en 60 segundos o menos dentro de la integración continua.`

## Casos borde

### CB-001

`SI una ruta se declara a la vez con concesión y con denegación de la misma especificidad, ENTONCES el permiso efectivo DEBE ser la denegación y la configuración DEBE registrar un hallazgo de solapamiento.`

### CB-002

`SI el rol solicita una ruta que su matriz no declara, ENTONCES el permiso efectivo DEBE ser la denegación y la operación DEBE detenerse con el hallazgo registrado.`

### CB-003

`SI el rol `auditor` recibe una solicitud de modificar un requisito o de escribir en una ruta de código, ENTONCES la operación DEBE quedar denegada y el hallazgo DEBE registrarse en el informe de auditoría.`

### CB-004

`SI el rol `coder` recibe una solicitud de escribir en una ruta fuera de `src/`, `tests/` y `tools/` que no sea el cierre de tareas, ENTONCES la operación DEBE quedar denegada y la tarea DEBE detenerse con el hallazgo registrado.`

### CB-005

`SI el rol `reviewer` recibe una solicitud de lanzar un subagente o de escribir en una ruta de código o de configuración, ENTONCES la operación DEBE quedar denegada.`

### CB-006

`SI la validación agregada o la suite de pruebas devuelve un código de salida distinto de cero, ENTONCES la integración continua DEBE finalizar en fallo y DEBE informar cuál de las dos falló.`

### CB-007

`SI la definición del flujo de integración continua contiene una instrucción de push, de creación de tag o de operación sobre el remoto, ENTONCES la revisión de la configuración DEBE registrar un error y el flujo NO DEBE integrarse.`

### CB-008

`SI la rama de integración no contiene el commit publicado en `main`, ENTONCES el hallazgo `AUD-081` NO DEBE registrarse como cerrado y DEBE consignarse el motivo.`

### CB-009

`SI la referencia remota obsoleta del release anterior figura en el listado de referencias, ENTONCES el hallazgo `AUD-082` NO DEBE registrarse como cerrado y DEBE consignarse el motivo.`

### CB-010

`SI una rama sin integración carece de decisión archivada y registrada, ENTONCES el hallazgo `AUD-083` NO DEBE registrarse como cerrado y DEBE consignarse el motivo.`

### CB-011

`SI existe un cambio de archivo ajeno a un commit, ENTONCES el hallazgo `AUD-084` NO DEBE registrarse como cerrado y DEBE consignarse el motivo.`

### CB-012

`SI un hecho operativo de `MEMORY.md` contradice el estado verificado del repositorio, ENTONCES el hallazgo `AUD-091` NO DEBE registrarse como cerrado y DEBE consignarse el motivo.`

### CB-013

`SI la prueba de configuración no puede ejecutarse sin escritura, ENTONCES el contraste DEBE limitarse a la comprobación de la declaración y DEBE registrarse como comprobación no verificada.`

### CB-014

`SI el rol `auditor` recibe una solicitud de aprobar una compuerta, ENTONCES DEBE rechazarla y DEBE registrar la solicitud en el informe de auditoría.`

### CB-015

`SI el rol `auditor` recibe una solicitud de escribir en una ruta de `docs/sdd/` cuyo nombre no cumple el patrón `auditoria_*.md`, ENTONCES la operación DEBE quedar denegada y el hallazgo DEBE registrarse en el informe de auditoría.`

### CB-016

`SI un Pull Request se dirige a una rama distinta de `dev` o de `main`, ENTONCES el flujo de integración continua NO DEBE ejecutarse y la verificación DEBE quedar a cargo de la ejecución local del validador y de la suite.`

### CB-017

`SI un rol solicita un comando de shell fuera de su allowlist, ENTONCES la operación DEBE quedar denegada y el hallazgo DEBE registrarse con el rol y el comando solicitado.`

## Fuera de alcance

- El cambio de regla en `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md` y las plantillas de rango 5: la base v2 se cierra en el bloque B1 del informe. En `AGENTS.md` solo se alinea el mapa de agentes con los seis roles de la constitución y en `MEMORY.md` solo se actualiza el estado operativo; una necesidad de cambio de regla se registra como dependencia y exige una spec de base.
- El cambio de `opencode.jsonc` más allá de la precedencia y de las protecciones de permisos: el archivo es configuración del cliente y no documento de la base.
- El enlace `CA → T`, la evidencia por tarea y el vínculo entre commit, merge y release: corresponden al bloque B4 del informe.
- La reescritura de las specs publicadas `SPEC-001` a `SPEC-007` y la alteración de `SPEC-008`, `SPEC-009` y `SPEC-010`.
- La instalación de un hook local de Git: la verificación de la integración se cubre con el flujo de integración continua.
- La configuración de la protección remota de ramas de GitHub: esta spec verifica el efecto del flujo y no la configuración del repositorio remoto.
- La gestión de claves y de la lista de firmantes: la mantiene el propietario.
- La declaración de compuertas: esta spec no aprueba G1, G4 ni G6.
- Los modelos, las cuantizaciones, el hardware y los benchmarks de ejecución local.

## Criterios de aceptación

### CA-001

`DADOS los seis roles de agente, CUANDO se inspecciona el archivo de cada rol en `.opencode/agents/`, ENTONCES declara sus permisos de lectura y de escritura por ruta, su allowlist de comandos de shell y su política de subagentes.`

Cubre: `RF-001`.

### CA-002

`DADO un rol con rutas concedidas y denegadas que se solapan, CUANDO se resuelve el permiso efectivo, ENTONCES la denegación explícita prevalece sobre la concesión, la ruta más específica prevalece sobre la general, la ruta no declarada queda denegada y una concesión de escritura no autoriza a declarar compuertas; y una ruta con concesión y denegación de la misma especificidad produce un hallazgo de configuración.`

Cubre: `RF-002`, `RNF-004`, `CB-001`, `CB-002`.

### CA-003

`DADO el rol `auditor`, CUANDO lee la base normativa y las specs, ENTONCES obtiene lectura completa y su escritura se limita a los informes `docs/sdd/auditoria_*.md`; y una solicitud de modificar un requisito, de escribir en una ruta de código o de escribir en una ruta de `docs/sdd/` ajena al patrón se rechaza con el hallazgo registrado en el informe.`

Cubre: `RF-003`, `CB-003`, `CB-015`.

### CA-004

`DADO el rol `auditor`, CUANDO se revisa su declaración y recibe una solicitud de aprobar una compuerta, ENTONCES su declaración reside en una sola ruta de `.opencode/agents/` como subagente con shell de solo lectura y subagentes denegados, la solicitud se rechaza y no se escribe línea de aprobación alguna.`

Cubre: `RNF-005`, `CB-014`.

### CA-005

`DADO el rol `reviewer`, CUANDO se le solicita lanzar un subagente o escribir en una ruta de código o de configuración, ENTONCES la operación queda denegada y su escritura se limita al reporte de validación de la spec en curso.`

Cubre: `RF-004`, `CB-005`.

### CA-006

`DADO el rol `coder`, CUANDO se le solicita escribir en una ruta fuera de `src/`, `tests/` y `tools/` que no sea el cierre de tareas, ENTONCES la operación queda denegada y la tarea se detiene con el hallazgo registrado.`

Cubre: `RF-005`, `CB-004`.

### CA-007

`DADO un Pull Request dirigido a `dev` o a `main`, CUANDO se ejecuta el flujo de integración continua, ENTONCES ejecuta la validación agregada del corpus y la suite de pruebas en un entorno Windows con Python 3.12, finaliza en fallo si cualquiera devuelve un código de salida distinto de cero, informa cuál falló, completa en 300 segundos o menos y la suite en 60 segundos o menos.`

Cubre: `RF-006`, `RNF-001`, `RNF-007`, `RNF-008`, `CB-006`.

### CA-008

`DADO el flujo de integración continua, CUANDO se inspecciona su definición en `.github/workflows/`, ENTONCES no contiene instrucción de push, de creación de tag ni de operación sobre el remoto y no requiere credenciales ni secretos; y una instrucción de esa clase produce error de configuración y el flujo no se integra.`

Cubre: `RF-007`, `RNF-002`, `CB-007`.

### CA-009

`DADOS los hallazgos `AUD-081` y `AUD-082`, CUANDO se verifica su estado, ENTONCES el reporte de validación acredita que la rama de integración contiene el commit publicado en `main` y que la referencia remota obsoleta del release anterior no figura en el listado de referencias; y si alguno de los dos hechos no se cumple, el hallazgo permanece abierto con el motivo consignado.`

Cubre: `RF-008`, `CB-008`, `CB-009`.

### CA-010

`DADOS los hallazgos `AUD-083` y `AUD-084`, CUANDO se verifica su estado, ENTONCES el reporte de validación acredita la decisión archivada de la rama sin integración y la ausencia de cambios ajenos a un commit; y una rama sin decisión registrada o un cambio sin commit mantiene el hallazgo abierto con el motivo consignado.`

Cubre: `RF-008`, `CB-010`, `CB-011`.

### CA-011

`DADO el hallazgo `AUD-091`, CUANDO se contrasta `MEMORY.md` con el estado del repositorio, ENTONCES cada hecho operativo coincide con el estado verificado y el cierre queda registrado en el reporte de validación con esa evidencia; y una contradicción mantiene el hallazgo abierto con el motivo consignado.`

Cubre: `RF-009`, `CB-012`.

### CA-012

`DADOS los permisos declarados por rol, CUANDO se ejecuta la prueba de configuración, ENTONCES informa por rol las rutas concedidas y las rutas denegadas, completa en 60 segundos o menos, no modifica archivos versionados y, si no puede ejecutarse sin escritura, se limita a la comprobación de la declaración y se registra como comprobación no verificada.`

Cubre: `RF-010`, `RNF-003`, `CB-013`.

### CA-013

`DADO `opencode.jsonc` con los permisos globales, CUANDO se compara con las matrices de rol, ENTONCES el orden de precedencia declarado coincide con las cuatro reglas de `RF-002`, ninguna concesión global amplía una denegación de rol y el archivo no contiene credenciales ni secretos.`

Cubre: `RF-011`, `RNF-006`.

### CA-014

`DADO un rol con su allowlist de comandos de shell, CUANDO solicita un comando fuera de ella, ENTONCES la operación queda denegada y el hallazgo se registra con el rol y el comando solicitado.`

Cubre: `CB-017`.

### CA-015

`DADO un Pull Request dirigido a una rama distinta de `dev` o de `main`, CUANDO se inspecciona el flujo de integración continua, ENTONCES el flujo no se dispara y la verificación queda a cargo de la ejecución local del validador y de la suite.`

Cubre: `RF-006`, `CB-016`.

### CA-016

`DADO el cierre de la implementación de esta spec, CUANDO se revisa `AGENTS.md`, ENTONCES menciona el rol `auditor` en el mapa de agentes, conserva entre 30 y 70 líneas útiles y no altera regla alguna de la base normativa.`

Cubre: `RF-012`.

### CA-017

`DADO el cierre de la implementación de esta spec, CUANDO se revisa `MEMORY.md`, ENTONCES menciona los seis roles de agente y la integración continua, y ningún hecho operativo suyo contradice el estado verificado del repositorio.`

Cubre: `RF-013`.

## Aprobaciones

<!-- Sección protegida: solo la escribe el propietario mediante un commit firmado. Dos casillas y ninguna más: G1 y G4. -->

- [x] G1: `- Approved by: Agent Sebaxtian` (2026-11-14)
- [x] G4: `- Approved by: Agent Sebaxtian` (2026-11-14)

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-11-14 | Redacción inicial de la spec |
| 0.2.0 | 2026-11-14 | Clarificación: ocho ambigüedades resueltas; precedencia de cuatro reglas y reflejo en `opencode.jsonc`; ruta y shell del rol `auditor`; disparadores, entorno y límites de la integración continua; evidencia de cierre de `AUD-081` a `AUD-084` y de `AUD-091`; alcance de `AGENTS.md` y de `MEMORY.md`; allowlist de shell por rol |
| 0.3.0 | 2026-11-14 | Plan: arquitectura de cinco capas, procedimiento de resolución de permisos, contratos de rol, configuración, flujo y pruebas, diez decisiones técnicas y matriz de cobertura de trece requisitos, ocho no funcionales y diecisiete casos borde |
| 0.4.0 | 2026-11-14 | Tareas: trece tareas atómicas con dependencias acíclicas, tres escritores declarados, una prueba positiva y un caso negativo por tarea de prueba, y cobertura completa de requisitos y casos borde |
| 0.5.0 | 2026-11-14 | Práctica operativa implementada con seis agentes, rol `auditor`, CI y 111 pruebas; revisión independiente con cuatro brechas cerradas y dictamen `CONVERGIDO` 38/38; G4 aprobada y estado `validated` |
| 0.6.0 | 2026-11-14 | Release v0.7.0 |

### Historial de transiciones

| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |
|---|---|---|---|---|---|
| 2026-11-14 | creación | — | `draft` | `planner` | redacción inicial de `spec.md` con once requisitos funcionales, cinco no funcionales, catorce casos borde y trece criterios de aceptación |
| 2026-11-14 | T1 | `draft` | `clarified` | `planner` | `clarify.md` cerrado con `AMB-001` a `AMB-008` resueltos, tres casos borde nuevos y los once parches marcados en `spec.md` |
| 2026-11-14 | T2 | `clarified` | `planned` | `planner` | línea de G1 firmada en `spec.md` en el commit `5b0d7f1` y `plan.md` escrito con diez decisiones y la matriz de cobertura de treinta y ocho filas |
| 2026-11-14 | T3 | `planned` | `tasked` | `planner` | `tasks.md` con trece tareas, ocho campos por tarea, dependencias acíclicas y cobertura de trece requisitos, ocho no funcionales y diecisiete casos borde |
| 2026-11-14 | T4 | `tasked` | `implementing` | orquestador | G2 verificada y ejecución agrupada autorizada; trece tareas cerradas con evidencia y 111 pruebas en verde |
| 2026-11-14 | T5 | `implementing` | `implemented` | orquestador | G3 con `OK: sin hallazgos`, trece tareas cerradas y 111 pruebas en verde |
| 2026-11-14 | T6 | `implemented` | `validated` | `reviewer` y G4 | `validation_report.md` con dictamen `CONVERGIDO` 38/38 y línea de G4 firmada en `spec.md` |
| 2026-11-14 | T7 | `validated` | `released` | `planner` | release v0.7.0 empaquetado con tag anotado pendiente de la firma de G6 |
