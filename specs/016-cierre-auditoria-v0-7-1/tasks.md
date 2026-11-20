# Tareas — SPEC-016

*Artefacto de rango 6: descomposición de `SPEC-016` en treinta y cuatro tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los 15 requisitos funcionales, los 9 requisitos no funcionales, los 13 casos borde y los 17 criterios de aceptación.*

## Regla de ejecución

La etapa cierra 11 observaciones con artefacto y 5 por ratificación firmada, regulariza 3 specs publicadas y fija el inventario único de hallazgos. Se ejecuta con seis escritores:

1. El rol `coder` escribe `tools/sdd/hallazgos.py`, `tools/sdd/validate.py` y `tools/sdd/tests/test_hallazgos.py`, ejecuta las suites y transcribe la evidencia de sus tareas en este archivo.
2. El rol `documenter` escribe `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, las 2 plantillas de rango 5, `docs/sdd/inventario_hallazgos.md`, `docs/sdd/README.md` y `CHANGELOG.md` dentro del alcance que declara cada tarea, como delegado explícito del propietario.
3. El rol `reviewer` escribe las 3 notas append-only de los reportes de `SPEC-013` y de `SPEC-015`, por delegación escrita del propietario, sin alterar matriz ni dictamen.
4. El rol `planner` escribe las 2 filas T7 de `T-030` en `specs/014-cierre-observaciones-finales/spec.md` y en `specs/015-cierre-auditoria-posterior/spec.md`, sus filas de motivo y este artefacto.
5. El propietario ejecuta `T-028` y `T-029`: firma el acta de ratificación en `docs/sdd/ratificacion_historica.md` y publica el cambio de `.opencode/agents/auditor.md`, ruta sin rol concesionario. Ningún agente escribe la línea de aprobación ni declara compuerta.
6. Las modificaciones de `T-030`, `T-031`, `T-032` y `T-033` tocan artefactos publicados de una spec, de modo que constan en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`. El rol declarado prepara el contenido y el propietario firma; el estado de firma se transcribe en la evidencia.

Reglas adicionales:

- Cada prueba se escribe en rojo antes de la tarea que la satisface y declara su caso positivo y su caso negativo.
- Una casilla se marca solo cuando la validación de la tarea se cumple; una validación fallida obliga a corregir el artefacto y a repetir la comprobación.
- Ninguna tarea declara evidencia antes de ejecutarse: el campo `Evidencia` fija qué se transcribe al cerrar.
- La etapa no modifica `src/`, `models/`, `bin/`, `llama.cpp/`, `.github/` ni los 5 informes de auditoría; no mueve ni recrea los tags `v0.7.0` y `v0.7.1`; no altera la matriz, el dictamen ni la línea de aprobación de los reportes publicados y no declara compuerta alguna.

## Referencias

- `spec.md`: `SPEC-016`, versión 0.4.0, estado `planned` al abrir esta etapa, 15 requisitos funcionales, 9 no funcionales, 13 casos borde y 17 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-21).
- `clarify.md`: cerrado con `AMB-001` a `AMB-016` resueltos y 21 parches aplicados a `spec.md`.
- `plan.md`: 12 componentes, contratos `C-1` a `C-9`, decisiones `DEC-001` a `DEC-008` y matriz de cobertura de 37 filas.
- `docs/sdd/auditoria_final_v0_7_1.md`: veredicto `NO CONFORME` sobre `5ba048d` con los 11 hallazgos que `T-024` cierra y las 3 observaciones parciales de severidad de origen.
- `docs/sdd/auditoria_cumplimiento_sdd.md`, `docs/sdd/auditoria_cierre_v0_7_0.md`, `docs/sdd/auditoria_final_v0_7_0.md` y `docs/sdd/auditoria_posterior_v0_7_0.md`: los 4 informes restantes que `T-020` a `T-023` inventarían.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea y la casilla `Completada`.
- `docs/sdd/README.md`: tabla de inventario de 36 filas de datos y regla de inventario de las líneas 67 a 73.
- `tools/sdd/validate.py`: comprobaciones `C-02`, `C-10`, `C-14` y `C-18`, y alcance impreso por la ejecución agregada.

## Progreso

- Cerradas: 0 de 34 tareas.
- Abiertas: 34 de 34 tareas; la prueba en rojo abre cada grupo y la verificación agregada es la última de la secuencia.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_hallazgos.py` | `T-001`, `T-003`, `T-006`, `T-008` | `coder` |
| 2 | `tools/sdd/hallazgos.py` | `T-002`, `T-004`, `T-005`, `T-007`, `T-009` | `coder` |
| 3 | `tools/sdd/validate.py` | `T-010`, `T-011` | `coder` |
| 4 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | `T-012` a `T-015` | `documenter` |
| 5 | `docs/sdd/plantillas/spec.md` | `T-016` | `documenter` |
| 6 | `docs/sdd/plantillas/informe_auditoria.md` | `T-017` | `documenter` |
| 7 | `docs/Flujo_de_Trabajo_Git.md` | `T-018` y `T-019` | `documenter` |
| 8 | `docs/sdd/inventario_hallazgos.md` | `T-020` a `T-025` | `documenter` |
| 9 | `docs/sdd/README.md` | `T-026` | `documenter` |
| 10 | `CHANGELOG.md` | `T-027` y `T-033` | `documenter` |
| 11 | `docs/sdd/ratificacion_historica.md` | `T-028` | propietario |
| 12 | `.opencode/agents/auditor.md` | `T-029` | propietario |
| 13 | `specs/014-cierre-observaciones-finales/spec.md` y `specs/015-cierre-auditoria-posterior/spec.md` | `T-030` | `planner` |
| 14 | `specs/013-cierre-reauditoria-conformidad/validation_report.md` y `specs/015-cierre-auditoria-posterior/validation_report.md` | `T-031` y `T-032` | `reviewer`, por delegación escrita del propietario |
| 15 | `specs/016-cierre-auditoria-v0-7-1/tasks.md` | evidencia de cada tarea y `T-034` | `coder` y `planner` |

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-013`, `CB-010`.
- **Criterio de aceptación:** `CA-014`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de las 4 condiciones del veredicto y de las 3 precedencias, y código de salida distinto de 0.
- **Evidencia:** salida transcrita de la ejecución en rojo, con el número de pruebas descubiertas y el nombre de cada prueba que falla por ausencia de la función `veredicto`.
- [ ] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-011`, `RF-013`, `CB-010`, `RNF-007`.
- **Criterio de aceptación:** `CA-012`, `CA-014`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para el grupo del veredicto, con `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` acreditados y la precedencia aplicada en ese orden.
- **Evidencia:** salida transcrita de la ejecución en verde, con el número de pruebas del grupo y el resultado de la prueba negativa de la fila con estado fuera del vocabulario.
- [ ] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-011`, `RF-012`, `CB-008`, `CB-009`, `CB-013`.
- **Criterio de aceptación:** `CA-012`, `CA-013`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba de compleción, la de la cita normativa y la del juicio sin regla, y código de salida distinto de 0.
- **Evidencia:** salida transcrita de la ejecución en rojo, con el nombre de cada prueba que falla por ausencia de `identificadores_de_informes` y de `regla_citada`.
- [ ] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`, `CB-013`, `RNF-005`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para la compleción, con 82 identificadores frente a 82 filas y 1 error con la ruta y el identificador en el texto sintético con 1 fila retirada.
- **Evidencia:** salida transcrita con el recuento de identificadores extraídos de los 5 informes, el recuento de filas del inventario y el mensaje del caso negativo.
- [ ] Completada.

### T-005

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-012`, `CB-009`, `RNF-006`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para la regla citada, con 1 error por fila sin la forma `ruta §capítulo:línea` y 0 errores sobre las 82 filas del inventario.
- **Evidencia:** salida transcrita con el recuento de filas sin cita, el identificador del caso negativo y el resultado del juicio sin regla tratado como observación.
- [ ] Completada.

### T-006

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-001`, `RF-003`, `RF-006`, `CB-003`, `CB-004`, `CB-006`.
- **Criterio de aceptación:** `CA-001`, `CA-003`, `CA-006`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba de los 6 artefactos, la del destino del tag y la de la autorreferencia, y código de salida distinto de 0.
- **Evidencia:** salida transcrita de la ejecución en rojo, con el nombre de cada prueba que falla por ausencia de `seis_artefactos`, `destino_del_tag` y `autorreferencia`.
- [ ] Completada.

### T-007

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-001`, `RF-003`, `RF-006`, `CB-003`, `CB-004`, `RNF-001`.
- **Criterio de aceptación:** `CA-001`, `CA-003`, `CA-006`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para los 6 artefactos, el destino del tag y la autorreferencia, con 0 coincidencias de autorreferencia sobre el contrato de `SPEC-016` y 1 error en el texto sintético de 5 claves.
- **Evidencia:** salida transcrita con las 6 claves de cada rango, el identificador del commit de merge de las 2 filas T7 y el recuento de coincidencias de autorreferencia.
- [ ] Completada.

### T-008

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-008`, `RF-009`, `RF-014`, `CB-001`, `CB-011`.
- **Criterio de aceptación:** `CA-008`, `CA-009`, `CA-015`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba del cierre de los 16 y de la del acta de ratificación, y código de salida distinto de 0.
- **Evidencia:** salida transcrita de la ejecución en rojo, con el nombre de cada prueba que falla por ausencia de `cierre_de_los_dieciseis` y de `ratificacion_admitida`.
- [ ] Completada.

### T-009

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-008`, `RF-009`, `RF-012`, `RF-013`, `CB-001`, `RNF-007`.
- **Criterio de aceptación:** `CA-008`, `CA-009`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para el cierre de los 16, con 11 filas en `cerrado` con evidencia por ruta y línea, 5 en `cerrado por ratificación` con identificador de commit y 1 caso negativo que deja vigente la observación sin artefacto.
- **Evidencia:** salida transcrita con el recuento por estado de las 16 filas y el mensaje del caso negativo de la observación sin artefacto.
- [ ] Completada.

### T-010

- **Dependencias:** `T-004`, `T-005`, `T-007`, `T-009`.
- **Requisitos cubiertos:** `RF-007`, `RF-011`, `RF-012`, `RF-013`, `CB-007`, `CB-013`.
- **Criterio de aceptación:** `CA-007`, `CA-012`, `CA-013`, `CA-014`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** `python tools\sdd\validate.py --all` con código de salida 0, las comprobaciones nuevas dentro del alcance impreso y la salida de la suite sin regresión sobre las 187 pruebas del corte.
- **Evidencia:** salida transcrita de `--all` con las comprobaciones incorporadas al alcance y el resultado de `python -m unittest discover -s tools\sdd\tests -q`.
- [ ] Completada.

### T-011

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-010`, `CB-003`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/validate.py`, `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde con la comprobación del historial de releases que admite las filas de historial de cambios y de transición y la constante que admite `released`, y 1 error en el texto sintético del release sin fila.
- **Evidencia:** salida transcrita con la prueba del historial en verde, el nombre del caso negativo y el recuento de filas admitidas sobre el `CHANGELOG.md` del corte.
- [ ] Completada.

### T-012

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-006`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §16 declara la prohibición de fijar el veredicto, el recuento de hallazgos y el conjunto de dimensiones de un informe posterior, la forma admitida del criterio limitada al artefacto y a su evidencia, y la consecuencia de un requisito con la forma prohibida.
- **Evidencia:** número de línea de la subsección nueva de §16 y transcripción literal de la prohibición, con el contraste de que la sección no altera las reglas existentes del capítulo.
- [ ] Completada.

### T-013

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `CB-009`, `CB-010`.
- **Criterio de aceptación:** `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:** §16 exige la regla citada por ruta, capítulo y línea, registra la observación fuera del recuento y transcribe la tabla de las 4 condiciones del veredicto con la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME`.
- **Evidencia:** número de línea de la subsección y transcripción de la tabla de condiciones y de la definición de observación y de tratamiento.
- [ ] Completada.

### T-014

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-007`, `CB-007`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** §12 declara que la fila de inventario de un informe de auditoría la escribe el `documenter` antes de la integración, limita la escritura del rol de auditoría al informe y declara el efecto de un informe integrado sin fila.
- **Evidencia:** número de línea del bloque nuevo de §12 y transcripción del alcance del rol de auditoría y del efecto de la fila ausente.
- [ ] Completada.

### T-015

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-003`, `CB-003`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §15 declara la tabla de los 6 artefactos con su modificación admitida, la exigencia de spec previa o fix previo para cualquier otra ruta y el orden en que el rango 3 se escribe antes que el rango 4.
- **Evidencia:** número de línea de la tabla y transcripción de las 6 filas con su modificación admitida.
- [ ] Completada.

### T-016

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-001`, `CB-006`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/plantillas/spec.md`.
- **Estimación:** 15 min.
- **Validación:** la lista de prohibiciones de la plantilla declara la prohibición de fijar el veredicto, el recuento de hallazgos y el conjunto de dimensiones de un informe posterior, y conserva las prohibiciones anteriores.
- **Evidencia:** número de línea de la prohibición nueva y transcripción de la lista de prohibiciones resultante.
- [ ] Completada.

### T-017

- **Dependencias:** `T-013`, `T-014`.
- **Requisitos cubiertos:** `RF-007`, `RF-012`, `RF-013`, `CB-007`, `CB-009`.
- **Criterio de aceptación:** `CA-007`, `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/plantillas/informe_auditoria.md`.
- **Estimación:** 30 min.
- **Validación:** la plantilla declara el campo de regla citada por ruta, capítulo y línea en cada hallazgo, la sección de observaciones fuera del recuento, el cálculo del veredicto desde el inventario y el cauce del `documenter` para la fila del corpus.
- **Evidencia:** número de línea de cada sección modificada y transcripción del campo de regla citada y de la sección de observaciones.
- [ ] Completada.

### T-018

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-003`, `CB-003`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** el paso 3 y la excepción de ramas de release declaran los 6 artefactos con los mismos 6 límites de §15, con la misma clave por artefacto y la exigencia de spec previa o fix previo.
- **Evidencia:** números de línea del paso 3 y de la excepción, y transcripción de las 6 filas con la comparación contra la tabla del rango 3.
- [ ] Completada.

### T-019

- **Dependencias:** `T-018`.
- **Requisitos cubiertos:** `RF-006`, `RF-015`, `CB-004`, `CB-012`, `RNF-009`.
- **Criterio de aceptación:** `CA-006`, `CA-016`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** la sección de validaciones de release exige la auditoría sobre el estado integrado en `dev` después de G5 y antes de G6, el veredicto `CONFORME` como condición del release, y el destino del tag en el commit de merge publicado en `main` con su ancestría respecto del commit de empaquetado.
- **Evidencia:** números de línea de la secuencia de release y del destino del tag, y transcripción de la condición del veredicto y del efecto de un veredicto distinto de `CONFORME`.
- [ ] Completada.

### T-020

- **Dependencias:** `T-013`, `T-017`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento declara la cabecera, el orden de los 8 campos, la convención de cita `ruta §capítulo:línea` y las 23 filas de las dimensiones D1 a D5 del informe de origen, con 23 identificadores distintos.
- **Evidencia:** recuento de filas del bloque, lista de los 23 identificadores y resultado de la comprobación de unicidad.
- [ ] Completada.

### T-021

- **Dependencias:** `T-020`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 25 min.
- **Validación:** el documento incorpora las 18 filas de las dimensiones D6 a D10 del informe de origen, con los 8 campos con contenido y sin repetir identificador.
- **Evidencia:** recuento acumulado de 41 filas, lista de los 18 identificadores añadidos y resultado de la comprobación de unicidad.
- [ ] Completada.

### T-022

- **Dependencias:** `T-021`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento incorpora las 23 filas de los 16 hallazgos del informe de cierre y los 7 del informe final, con el estado que cada informe declara y su fecha de corte.
- **Evidencia:** recuento acumulado de 64 filas y lista de los 23 identificadores añadidos con el estado declarado.
- [ ] Completada.

### T-023

- **Dependencias:** `T-022`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento incorpora las 18 filas de los 10 hallazgos del informe posterior y los 8 del informe de `v0.7.1`, con el estado `parcial` o `vigente` que esos informes declaran y la evidencia por ruta y línea.
- **Evidencia:** recuento acumulado de 82 filas, lista de los 18 identificadores añadidos con su estado y resultado de la comprobación de 82 filas para 82 identificadores.
- [ ] Completada.

### T-024

- **Dependencias:** `T-023`, `T-028`.
- **Requisitos cubiertos:** `RF-009`, `RF-014`, `CB-001`, `CB-011`.
- **Criterio de aceptación:** `CA-009`, `CA-015`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** las 16 filas del cierre declaran `cerrado` en las 11 cerradas por artefacto y `cerrado por ratificación` en las 5 cubiertas por el acta, con la evidencia por ruta y línea o el identificador del commit firmado.
- **Evidencia:** recuento de 16 filas por estado, identificador del commit del acta y resultado de la comprobación de evidencia no vacía en las 16 filas.
- [ ] Completada.

### T-025

- **Dependencias:** `T-024`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `CB-009`.
- **Criterio de aceptación:** `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 20 min.
- **Validación:** la sección de observaciones y tratamientos declara el juicio sin regla citada, su severidad, la fecha y el identificador del commit del tratamiento, y el veredicto calculado desde las 82 filas con su recuento de abiertos.
- **Evidencia:** transcripción del recuento de hallazgos abiertos, del recuento de observaciones de severidad `Alta` o `Media` sin tratamiento y del veredicto resultante.
- [ ] Completada.

### T-026

- **Dependencias:** `T-020`, `T-028`.
- **Requisitos cubiertos:** `RF-007`, `RF-011`, `CB-007`.
- **Criterio de aceptación:** `CA-007`, `CA-012`.
- **Archivos:** `docs/sdd/README.md`.
- **Estimación:** 20 min.
- **Validación:** la tabla de inventario del corpus porta la fila de `docs/sdd/inventario_hallazgos.md` y la de `docs/sdd/ratificacion_historica.md`, desplaza la fila de `firmantes_autorizados` sin repetir el orden de lectura y conserva 1 fila por archivo.
- **Evidencia:** números de fila de las 2 filas nuevas, orden de lectura resultante y salida de `test_inventario_del_corpus` en verde.
- [ ] Completada.

### T-027

- **Dependencias:** `T-019`, `T-028`.
- **Requisitos cubiertos:** `RF-003`, `RF-005`, `RF-010`, `RNF-004`.
- **Criterio de aceptación:** `CA-003`, `CA-005`, `CA-010`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 30 min.
- **Validación:** `Unreleased` declara el conjunto de 6 artefactos, la regularización del historial de releases, el inventario de hallazgos, la prohibición de autorreferencia, el identificador `564bac4` y `494db2e` con sus 3 rutas publicadas y el efecto declarativo de la ratificación, sin línea de aprobación.
- **Evidencia:** transcripción de las viñetas añadidas a `Unreleased` y número de línea del inicio de la sección.
- [ ] Completada.

### T-028

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-004`, `RF-014`, `CB-002`, `CB-011`, `RNF-008`.
- **Criterio de aceptación:** `CA-004`, `CA-015`.
- **Archivos:** `docs/sdd/ratificacion_historica.md`.
- **Estimación:** 30 min.
- **Validación:** el acta declara la fecha UTC, los 5 identificadores de exención, los 2 identificadores de commit con sus rutas publicadas, el efecto retroactivo limitado al régimen y la referencia a `docs/sdd/firmantes_autorizados`, dentro de 1 commit con estado de firma `G`.
- **Evidencia:** `git show --no-patch --format=%G?` y `%GK` del commit del acta, con la huella de la clave contrastada contra `docs/sdd/firmantes_autorizados`.
- [ ] Completada.

### T-029

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-007`, `CB-007`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `.opencode/agents/auditor.md`.
- **Estimación:** 20 min.
- **Validación:** la descripción y el cuerpo del rol declaran que el auditor no escribe la fila del inventario de hallazgos ni la fila del corpus, que su escritura se limita a `docs/sdd/auditoria_*.md` y que cita la regla incumplida en cada hallazgo; la suite de permisos sigue en verde.
- **Evidencia:** transcripción del bloque de alcance y salida de `python -m unittest tools.sdd.tests.test_agent_permissions -q` con las pruebas de la matriz del rol en verde.
- [ ] Completada.

### T-030

- **Dependencias:** `T-019`.
- **Requisitos cubiertos:** `RF-006`, `CB-004`, `RNF-002`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/014-cierre-observaciones-finales/spec.md`, `specs/015-cierre-auditoria-posterior/spec.md`.
- **Estimación:** 30 min.
- **Validación:** cada fila T7 declara el commit de merge publicado en `main`, su identificador y la ancestría con el commit de empaquetado, conserva el destino `released`, el campo `release` y el identificador del release, e incrementa 1 incremento PATCH con 1 fila de motivo por corrección.
- **Evidencia:** transcripción de las 2 filas T7 corregidas, versiones resultantes 0.8.2 y las 2 filas de motivo añadidas.
- [ ] Completada.

### T-031

- **Dependencias:** `T-012`, `T-016`.
- **Requisitos cubiertos:** `RF-002`, `CB-006`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/validation_report.md`, `specs/015-cierre-auditoria-posterior/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** cada reporte porta 1 nota append-only con la regla de `RF-001` y la declaración de que el veredicto y el recuento los emite el rol de auditoría, con 0 líneas retiradas y la matriz y el dictamen conservados.
- **Evidencia:** números de línea de las 2 notas, recuento de líneas retiradas de cada documento y resultado de la comprobación de autorreferencia sobre las 2 specs.
- [ ] Completada.

### T-032

- **Dependencias:** `T-019`.
- **Requisitos cubiertos:** `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `specs/015-cierre-auditoria-posterior/validation_report.md`.
- **Estimación:** 25 min.
- **Validación:** la nota append-only transcribe el resultado de G5, el resultado de G6 y el objeto anotado del tag `v0.7.1` con su mensaje y su commit objetivo, conserva la transcripción previa de la línea 77 y no altera la matriz ni el dictamen.
- **Evidencia:** número de línea inicial de la nota, transcripción del objeto del tag y recuento de líneas retiradas del documento.
- [ ] Completada.

### T-033

- **Dependencias:** `T-032`.
- **Requisitos cubiertos:** `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 20 min.
- **Validación:** la entrada `v0.7.1` porta 1 bloque de registro con el resultado de G5 y de G6 y con el objeto del tag, y conserva la línea de aprobación y el bloque de cambios.
- **Evidencia:** número de línea del bloque y transcripción del resultado de las 2 compuertas y del objeto del tag.
- [ ] Completada.

### T-034

- **Dependencias:** `T-010`, `T-011`, `T-024`, `T-025`, `T-026`, `T-027`, `T-029`, `T-030`, `T-031`, `T-032`, `T-033`.
- **Requisitos cubiertos:** `RF-015`, `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004`, `RNF-005`, `RNF-006`, `RNF-007`, `RNF-008`, `RNF-009`.
- **Criterio de aceptación:** `CA-011`, `CA-017`.
- **Archivos:** `specs/016-cierre-auditoria-v0-7-1/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python tools\sdd\validate.py --all` con código de salida 0 en 300 segundos o menos, 0 hallazgos sin fila, 0 campos obligatorios vacíos, 0 filas sin regla citada, 0 diferencias de veredicto, 0 violaciones históricas sin ratificación firmada y 0 requisitos de esta spec que fijen el veredicto de un informe posterior.
- **Evidencia:** salida transcrita de `--all` con los 7 recuentos de `CA-017`, la duración de la ejecución y el estado de firma del commit de las modificaciones publicadas.
- [ ] Completada.
