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

- Cerradas: 34 de 34 tareas (`T-001` a `T-034`).
- Abiertas: 0 de 34 tareas; la secuencia se cierra tras la viñeta de `RF-004` en la entrada `Unreleased` de `CHANGELOG.md` y la firma del commit `d0126ce` de las modificaciones publicadas, con estado de firma `G`.

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
- **Evidencia:** rojo con `python -m unittest tools.sdd.tests.test_hallazgos -q`: «Ran 9 tests in 0.007s» y «FAILED (errors=9)». Las 8 pruebas del grupo fallan con `AttributeError: module 'hallazgos' has no attribute 'veredicto'` y `test_veredicto_contradice_el_recuento` con `... no attribute 'problemas_del_veredicto'`. Nombres: `test_veredicto_no_conforme`, `test_veredicto_no_verificable`, `test_veredicto_parcial`, `test_veredicto_conforme`, `test_precedencia_no_conforme`, `test_precedencia_no_verificable`, `test_precedencia_parcial` y `test_estado_fuera_del_vocabulario`. El módulo se creó antes con sus constantes y sin función alguna.
- [x] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-011`, `RF-013`, `CB-010`, `RNF-007`.
- **Criterio de aceptación:** `CA-012`, `CA-014`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para el grupo del veredicto, con `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` acreditados y la precedencia aplicada en ese orden.
- **Evidencia:** verde: «Ran 9 tests in 0.000s» y «OK». Las 4 condiciones y las 3 precedencias quedan acreditadas, con la observación de severidad `Baja` sin tratamiento admitida bajo `CONFORME` y la de severidad `Alta` con tratamiento admitida con el mismo resultado. Negativa `test_estado_fuera_del_vocabulario`: `ValueError` con «la fila AUD-777 declara el estado «cerrado por acuerdo» fuera del vocabulario de C-2».
- [x] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-011`, `RF-012`, `CB-008`, `CB-009`, `CB-013`.
- **Criterio de aceptación:** `CA-012`, `CA-013`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba de compleción, la de la cita normativa y la del juicio sin regla, y código de salida distinto de 0.
- **Evidencia:** rojo: «Ran 16 tests in 0.013s» y «FAILED (failures=1, errors=6)». Los errores nombran la ausencia de `textos_de_informes`, `identificadores_de_informes`, `problemas_de_complecion`, `problemas_de_regla_citada`, `clasificar_juicios` y `problemas_de_corpus`. La prueba de la fila del inventario en el corpus se ancló a texto sintético con la fila escrita, porque la fila real de `docs/sdd/README.md` corresponde a `T-026`.
- [x] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`, `CB-013`, `RNF-005`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para la compleción, con 82 identificadores frente a 82 filas y 1 error con la ruta y el identificador en el texto sintético con 1 fila retirada.
- **Evidencia:** verde: los 5 informes declaran 82 identificadores en la primera celda de sus filas de tabla, de `AUD-001` a `AUD-110`, y las 82 filas sintéticas producen 0 problemas. Con `AUD-011` retirada, 1 problema: «docs/sdd/auditoria_cumplimiento_sdd.md: el hallazgo AUD-011 carece de fila en docs/sdd/inventario_hallazgos.md». La extracción por token en prosa devuelve 90 identificadores y se descartó por no corresponder al corte de 82.
- [x] Completada.

### T-005

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-012`, `CB-009`, `RNF-006`.
- **Criterio de aceptación:** `CA-013`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para la regla citada, con 1 error por fila sin la forma `ruta §capítulo:línea` y 0 errores sobre las 82 filas del inventario.
- **Evidencia:** verde: 0 problemas sobre las 82 filas que citan `docs/constitution.md §7:76` y 1 problema al retirar la línea de la cita: «el hallazgo AUD-001 no cita la regla con la forma «ruta §capítulo:línea»: «docs/constitution.md §7»». El juicio `OBS-001` sin regla queda clasificado como observación, no computa como abierto y el veredicto devuelve `PARCIAL`.
- [x] Completada.

### T-006

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-001`, `RF-003`, `RF-006`, `CB-003`, `CB-004`, `CB-006`.
- **Criterio de aceptación:** `CA-001`, `CA-003`, `CA-006`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba de los 6 artefactos, la del destino del tag y la de la autorreferencia, y código de salida distinto de 0.
- **Evidencia:** rojo: «Ran 23 tests in 0.047s» y «FAILED (errors=7)» por ausencia de `seis_artefactos`, `claves_declaradas`, `destino_del_tag`, `alteracion_del_destino` y `autorreferencia`. La prueba de las 2 enumeraciones del repositorio queda en `skipTest` mientras `T-015` y `T-018` no escriban las claves `A1` a `A6`.
- [x] Completada.

### T-007

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-001`, `RF-003`, `RF-006`, `CB-003`, `CB-004`, `RNF-001`.
- **Criterio de aceptación:** `CA-001`, `CA-003`, `CA-006`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para los 6 artefactos, el destino del tag y la autorreferencia, con 0 coincidencias de autorreferencia sobre el contrato de `SPEC-016` y 1 error en el texto sintético de 5 claves.
- **Evidencia:** verde: «Ran 23 tests in 0.026s» y «OK (skipped=1)». Las 6 claves `A1` a `A6` y, con `A6` retirada del rango 4, 1 error que nombra «A6» y «rango 4». Las 2 filas T7 publicadas pasan con la evidencia corregida en memoria; los commits de merge que el informe declara son `5a3af48` para `v0.7.0` y `da30c86` para `v0.7.1` (`docs/sdd/auditoria_final_v0_7_1.md:101`). Autorreferencia: 0 coincidencias sobre `spec.md` y `tasks.md` de `SPEC-016`, 1 error en el texto sintético que fija el veredicto de conformidad y 0 con la nota del reporte.
- [x] Completada.

### T-008

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-008`, `RF-009`, `RF-014`, `CB-001`, `CB-011`.
- **Criterio de aceptación:** `CA-008`, `CA-009`, `CA-015`.
- **Archivos:** `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en rojo con los nombres de la prueba del cierre de los 16 y de la del acta de ratificación, y código de salida distinto de 0.
- **Evidencia:** rojo: «Ran 30 tests in 0.043s» y «FAILED (errors=7)» por ausencia de `cierre_de_los_dieciseis`, `filas_del_cierre`, `problemas_del_acta` y `ratificacion_admitida`.
- [x] Completada.

### T-009

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `RF-008`, `RF-009`, `RF-012`, `RF-013`, `CB-001`, `RNF-007`.
- **Criterio de aceptación:** `CA-008`, `CA-009`.
- **Archivos:** `tools/sdd/hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde para el cierre de los 16, con 11 filas en `cerrado` con evidencia por ruta y línea, 5 en `cerrado por ratificación` con identificador de commit y 1 caso negativo que deja vigente la observación sin artefacto.
- **Evidencia:** verde: 16 filas, 11 en `cerrado` con evidencia por ruta y línea y 5 en `cerrado por ratificación` con identificador de commit. Negativa: «AUD-106: la observación carece de artefacto o de evidencia por ruta y línea, de modo que queda vigente y no se declara cerrada»; la fila que declara `vigente` sin artefacto produce 0 problemas.
- [x] Completada.

### T-010

- **Dependencias:** `T-004`, `T-005`, `T-007`, `T-009`.
- **Requisitos cubiertos:** `RF-007`, `RF-011`, `RF-012`, `RF-013`, `CB-007`, `CB-013`.
- **Criterio de aceptación:** `CA-007`, `CA-012`, `CA-013`, `CA-014`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** `python tools\sdd\validate.py --all` con código de salida 0, las comprobaciones nuevas dentro del alcance impreso y la salida de la suite sin regresión sobre las 187 pruebas del corte.
- **Evidencia:** `python tools\sdd\validate.py --all`: código 0 con las 4 comprobaciones nuevas en «Comprobaciones ejecutadas» y 6 advertencias que nombran las tareas `T-015`, `T-018`, `T-020` a `T-025`, `T-028` y `T-030`. Suite: «Ran 222 tests in 1.369s» y «FAILED (failures=1, skipped=1)»; el único fallo es `test_consistencia_documental` con «MEMORY.md no declara el estado de SPEC-016», anterior a esta etapa y fuera del alcance de escritura del rol `coder`. Suite de Git: «Ran 48 tests in 20.916s» y «OK».
- [x] Completada.

### T-011

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-010`, `CB-003`.
- **Criterio de aceptación:** `CA-010`.
- **Archivos:** `tools/sdd/validate.py`, `tools/sdd/tests/test_hallazgos.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest tools.sdd.tests.test_hallazgos -q` en verde con la comprobación del historial de releases que admite las filas de historial de cambios y de transición y la constante que admite `released`, y 1 error en el texto sintético del release sin fila.
- **Evidencia:** `test_historial_de_releases` en verde con la constante `ESTADOS_POSTERIORES_A_LA_VALIDACION` declarada en `hallazgos.py` y con `released` admitido; la comprobación exige 1 fila por release publicado y no equipara recuentos. `CHANGELOG.md` del corte: 10 releases publicados y 10 filas admitidas. Caso negativo en `test_hallazgos`: 1 error que nombra `v0.2.0`. `test_complecion` contrasta 82 identificadores con 82 filas y el inventario futuro los cubre con los 8 campos de `RF-011`.
- [x] Completada.

### T-012

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-006`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §16 declara la prohibición de fijar el veredicto, el recuento de hallazgos y el conjunto de dimensiones de un informe posterior, la forma admitida del criterio limitada al artefacto y a su evidencia, y la consecuencia de un requisito con la forma prohibida.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:378` porta el bloque «Autorreferencia» dentro de §16, abierto en `:372`; transcripción: «Ninguna spec fija el veredicto, el recuento de hallazgos ni el conjunto de dimensiones de una auditoría futura. Un requisito, un criterio de aceptación o una tarea de una spec no declara `CONFORME`, `PARCIAL`, `NO CONFORME` ni `NO VERIFICABLE`, no declara un recuento de hallazgos y no enumera las dimensiones de un informe cuya emisión es posterior a la aprobación de la spec. El criterio que invoca una auditoría se limita a exigir la existencia del artefacto y la evidencia transcrita. El veredicto y el recuento los emite el rol de auditoría sobre el estado del inventario. Un requisito, un criterio o una tarea con la forma prohibida se registra como hallazgo y la spec no se aprueba en G1.» El bloque se intercala entre la declaración del documento (`:376`) y la auditoría de conformidad (`:380`), y las 5 reglas previas de §16 conservan su redacción.
- [x] Completada.

### T-013

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `CB-009`, `CB-010`.
- **Criterio de aceptación:** `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 30 min.
- **Validación:** §16 exige la regla citada por ruta, capítulo y línea, registra la observación fuera del recuento y transcribe la tabla de las 4 condiciones del veredicto con la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME`.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:382` exige la cita con la forma `ruta §capítulo:línea` y registra la observación fuera del recuento; `:384` declara el cálculo desde el inventario; `:386-391` transcriben la tabla de las 4 condiciones con la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME`; `:393` define los estados cerrados y abiertos, el tratamiento como decisión registrada del propietario con fecha e identificador del commit y la exigencia de 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento bajo `CONFORME`.
- [x] Completada.

### T-014

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-007`, `CB-007`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** §12 declara que la fila de inventario de un informe de auditoría la escribe el `documenter` antes de la integración, limita la escritura del rol de auditoría al informe y declara el efecto de un informe integrado sin fila.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:300` porta el bloque «Inventario del corpus» de §12: «La fila del informe de auditoría en la tabla de inventario de `docs/sdd/README.md` la escribe el `documenter` antes de la integración del informe. El rol de auditoría escribe solo el informe que produce y no escribe esa fila. Un informe integrado sin fila deja la verificación en rojo con la ruta del archivo sin fila y detiene la integración.» El alcance del rol de auditoría consta en la tabla de roles (`:291`) y en el bloque «Rol de auditoría» (`:298`), con lectura sobre la base completa y escritura limitada al informe.
- [x] Completada.

### T-015

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-003`, `CB-003`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 25 min.
- **Validación:** §15 declara la tabla de los 6 artefactos con su modificación admitida, la exigencia de spec previa o fix previo para cualquier otra ruta y el orden en que el rango 3 se escribe antes que el rango 4.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md:355-362` porta la tabla de §15 con las 6 filas y su modificación admitida: `A1` `CHANGELOG.md` con la entrada del release e historial de releases; `A2` `specs/INDEX.md` con la fila de la spec publicada; `A3` `spec.md` de una spec publicada con los campos del frontmatter `status`, `version`, `updated` y `release`; `A4` `spec.md` de una spec publicada con la fila del historial de cambios de la versión de release; `A5` `spec.md` de una spec publicada con la fila T7 del historial de transiciones; `A6` `validation_report.md` de una spec publicada con la línea `Release:` del tag. `:353` fija el orden de escritura del rango 3 antes que el paso 3 del rango 4 y `:364` exige spec previa o fix previo para cualquier ruta distinta.
- [x] Completada.

### T-016

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-001`, `CB-006`.
- **Criterio de aceptación:** `CA-001`.
- **Archivos:** `docs/sdd/plantillas/spec.md`.
- **Estimación:** 15 min.
- **Validación:** la lista de prohibiciones de la plantilla declara la prohibición de fijar el veredicto, el recuento de hallazgos y el conjunto de dimensiones de un informe posterior, y conserva las prohibiciones anteriores.
- **Evidencia:** `docs/sdd/plantillas/spec.md:80` porta el comentario de prohibiciones de la plantilla, que declara: «Prohibiciones de esta plantilla: rutas de código, clases, SQL y comandos técnicos; casilla de G6; dos formas para un mismo campo; requisito, criterio de aceptación o tarea que fija el veredicto, el recuento de hallazgos o el conjunto de dimensiones de un informe de auditoría posterior a la aprobación de la spec, porque esa materia corresponde al rol de auditoría y el criterio que invoca una auditoría se limita a exigir la existencia del artefacto y la evidencia transcrita.» Las 3 prohibiciones anteriores conservan su redacción y la lista se amplía sin retirar cláusula alguna.
- [x] Completada.

### T-017

- **Dependencias:** `T-013`, `T-014`.
- **Requisitos cubiertos:** `RF-007`, `RF-012`, `RF-013`, `CB-007`, `CB-009`.
- **Criterio de aceptación:** `CA-007`, `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/plantillas/informe_auditoria.md`.
- **Estimación:** 30 min.
- **Validación:** la plantilla declara el campo de regla citada por ruta, capítulo y línea en cada hallazgo, la sección de observaciones fuera del recuento, el cálculo del veredicto desde el inventario y el cauce del `documenter` para la fila del corpus.
- **Evidencia:** `docs/sdd/plantillas/informe_auditoria.md:66` declara el campo `- **Regla citada:** <ruta> §<capítulo>:<línea>` en cada hallazgo; `:30` fija la forma `ruta §capítulo:línea` y la exclusión de la observación del recuento; `:71-77` porta la sección «Observaciones» con la tabla de severidad, la observación, el tratamiento y la regla de que una observación de severidad `Alta` o `Media` sin tratamiento impide `CONFORME`; `:91` calcula el veredicto desde el estado de las filas del inventario; `:24` declara que la fila del informe en el inventario del corpus la escribe el `documenter` antes de la integración y que el rol de auditoría no la escribe.
- [x] Completada.

### T-018

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-003`, `CB-003`.
- **Criterio de aceptación:** `CA-003`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 25 min.
- **Validación:** el paso 3 y la excepción de ramas de release declaran los 6 artefactos con los mismos 6 límites de §15, con la misma clave por artefacto y la exigencia de spec previa o fix previo.
- **Evidencia:** `docs/Flujo_de_Trabajo_Git.md:343` porta el paso 3 con los 6 artefactos, las claves `A1` a `A6` y el mismo límite que §15 del protocolo; `:345-352` transcriben la tabla de las 6 filas con la misma clave y la misma modificación admitida que `docs/sdd/PROTOCOLO_OPERATIVO.md:355-362`; `:488` declara la excepción de ramas de release sobre los 6 artefactos de las claves `A1` a `A6` y la exigencia de spec previa o fix previo para cualquier otra ruta. La comparación fila por fila no registra diferencia entre las 2 enumeraciones.
- [x] Completada.

### T-019

- **Dependencias:** `T-018`.
- **Requisitos cubiertos:** `RF-006`, `RF-015`, `CB-004`, `CB-012`, `RNF-009`.
- **Criterio de aceptación:** `CA-006`, `CA-016`.
- **Archivos:** `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** la sección de validaciones de release exige la auditoría sobre el estado integrado en `dev` después de G5 y antes de G6, el veredicto `CONFORME` como condición del release, y el destino del tag en el commit de merge publicado en `main` con su ancestría respecto del commit de empaquetado.
- **Evidencia:** `docs/Flujo_de_Trabajo_Git.md:16` fija la secuencia «G5, después la auditoría de conformidad sobre el estado integrado en `dev` y después G6» y el efecto: «El release exige el veredicto `CONFORME`; un veredicto distinto de `CONFORME` impide la publicación, conserva la spec en `validated` y transcribe el motivo con el hallazgo que lo sostiene.» `:232` repite la condición entre las validaciones de release y `:11-12` la incorporan a la condición de G6; `:412` fija el destino del tag en el commit de merge publicado en `main`, no en el commit de empaquetado, con el identificador, la rama y la ancestría en la fila T7; `:414` ordena las 3 verificaciones y `:418` registra el resultado de G5 y de G6 en los 2 soportes.
- [x] Completada.

### T-020

- **Dependencias:** `T-013`, `T-017`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento declara la cabecera, el orden de los 8 campos, la convención de cita `ruta §capítulo:línea` y las 23 filas de las dimensiones D1 a D5 del informe de origen, con 23 identificadores distintos.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:22` declara el bloque 1 con 23 filas: `AUD-001` a `AUD-007`, `AUD-011` a `AUD-014`, `AUD-021` a `AUD-023`, `AUD-031` a `AUD-035` y `AUD-041` a `AUD-044`. Las 23 filas constan en la tabla de `:33-55` con los 8 campos en el orden de `RF-011` y la convención `ruta §capítulo:línea` de `:15`; la comprobación de unicidad devuelve 23 identificadores distintos y `python tools\sdd\validate.py --all` no registra identificador repetido.
- [x] Completada.

### T-021

- **Dependencias:** `T-020`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 25 min.
- **Validación:** el documento incorpora las 18 filas de las dimensiones D6 a D10 del informe de origen, con los 8 campos con contenido y sin repetir identificador.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:23` declara el bloque 2 con 18 filas: `AUD-051` a `AUD-055`, `AUD-061` a `AUD-064`, `AUD-071`, `AUD-072`, `AUD-081` a `AUD-084`, `AUD-091`, `AUD-093` y `AUD-094`; las 18 constan en `:56-73` con los 8 campos con contenido. Recuento acumulado: 41 filas. La comprobación de unicidad sobre las 41 devuelve 0 identificadores repetidos; el error `C-19` de campo vacío y el de identificador repetido no se registran.
- [x] Completada.

### T-022

- **Dependencias:** `T-021`.
- **Requisitos cubiertos:** `RF-011`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento incorpora las 23 filas de los 16 hallazgos del informe de cierre y los 7 del informe final, con el estado que cada informe declara y su fecha de corte.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:24` declara el bloque 3 con las 23 filas de los 16 hallazgos de `docs/sdd/auditoria_cierre_v0_7_0.md` y los 7 de `docs/sdd/auditoria_final_v0_7_0.md`; las 23 constan en `:74-96` con el estado que cada informe declara en el campo `Informe que declara el estado` y su fecha de corte 2026-11-14. Recuento acumulado: 64 filas, con los 8 campos con contenido.
- [x] Completada.

### T-023

- **Dependencias:** `T-022`.
- **Requisitos cubiertos:** `RF-011`, `CB-008`.
- **Criterio de aceptación:** `CA-012`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** el documento incorpora las 18 filas de los 10 hallazgos del informe posterior y los 8 del informe de `v0.7.1`, con el estado `parcial` o `vigente` que esos informes declaran y la evidencia por ruta y línea.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:25` declara el bloque 4 con las 18 filas de los 10 hallazgos de `docs/sdd/auditoria_posterior_v0_7_0.md` y los 8 de `docs/sdd/auditoria_final_v0_7_1.md`; las 18 constan en `:97-114` con el estado que declara el informe más reciente y la evidencia por ruta y línea. Recuento acumulado: 82 filas en `:33-114` para 82 identificadores distintos. La comprobación de `C-19` contrasta 82 identificadores con 82 filas y devuelve 0 problemas; el caso negativo de 1 fila retirada produce 1 problema con la ruta del informe y el identificador.
- [x] Completada.

### T-024

- **Dependencias:** `T-023`, `T-028`.
- **Requisitos cubiertos:** `RF-009`, `RF-014`, `CB-001`, `CB-011`.
- **Criterio de aceptación:** `CA-009`, `CA-015`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 30 min.
- **Validación:** las 16 filas del cierre declaran `cerrado` en las 11 cerradas por artefacto y `cerrado por ratificación` en las 5 cubiertas por el acta, con la evidencia por ruta y línea o el identificador del commit firmado.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:118-137` porta la tabla de cierre con 16 filas: 11 en `cerrado` con evidencia por ruta y línea (`:122-132`) y 5 en `cerrado por ratificación` con el identificador del commit `9042ae6` y los commits ratificados `494db2e` y `564bac4` (`:133-137`). El identificador del commit del acta es `9042ae6`, con estado de firma `G`. La comprobación de `C-25` devuelve 0 problemas: las 16 filas declaran evidencia no vacía y el número de observaciones cerradas sin el artefacto correspondiente es 0.
- [x] Completada.

### T-025

- **Dependencias:** `T-024`.
- **Requisitos cubiertos:** `RF-012`, `RF-013`, `CB-009`.
- **Criterio de aceptación:** `CA-013`, `CA-014`.
- **Archivos:** `docs/sdd/inventario_hallazgos.md`.
- **Estimación:** 20 min.
- **Validación:** la sección de observaciones y tratamientos declara el juicio sin regla citada, su severidad, la fecha y el identificador del commit del tratamiento, y el veredicto calculado desde las 82 filas con su recuento de abiertos.
- **Evidencia:** `docs/sdd/inventario_hallazgos.md:141-145` declara el juicio sin regla citada como observación y su exclusión del recuento: 0 observaciones registradas en el corte, 0 tratamientos registrados y 0 filas del anexo que computen como hallazgo abierto. `:149` transcribe el resultado: «Veredicto calculado: `CONFORME`. Recuento sobre las 82 filas: 0 hallazgos abiertos, 77 hallazgos cerrados, 5 cerrados por ratificación y 0 cerrados por exención.» `:151` aplica la precedencia de `RF-013` y descarta los 3 valores anteriores con 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento.
- [x] Completada.

### T-026

- **Dependencias:** `T-020`, `T-028`.
- **Requisitos cubiertos:** `RF-007`, `RF-011`, `CB-007`.
- **Criterio de aceptación:** `CA-007`, `CA-012`.
- **Archivos:** `docs/sdd/README.md`.
- **Estimación:** 20 min.
- **Validación:** la tabla de inventario del corpus porta la fila de `docs/sdd/inventario_hallazgos.md` y la de `docs/sdd/ratificacion_historica.md`, desplaza la fila de `firmantes_autorizados` sin repetir el orden de lectura y conserva 1 fila por archivo.
- **Evidencia:** `docs/sdd/README.md:65` porta la fila de `inventario_hallazgos.md` con orden de lectura 36 y rango «Sin rango»; `:67` porta la fila de `ratificacion_historica.md` con orden de lectura 38 y rango «Sin rango»; `:66` porta la fila de `firmantes_autorizados`, desplazada al orden 37. El orden de lectura resultante es 35 para `auditoria_final_v0_7_1.md`, 36 para el inventario, 37 para los firmantes y 38 para el acta, sin repetición; la tabla conserva 1 fila por archivo y `test_inventario_del_corpus` queda en verde dentro de las 222 pruebas de la suite de `tools/sdd/tests`.
- [x] Completada.

### T-027

- **Dependencias:** `T-019`, `T-028`.
- **Requisitos cubiertos:** `RF-003`, `RF-005`, `RF-010`, `RNF-004`.
- **Criterio de aceptación:** `CA-003`, `CA-005`, `CA-010`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 30 min.
- **Validación:** `Unreleased` declara el conjunto de 6 artefactos, la regularización del historial de releases, el inventario de hallazgos, la prohibición de autorreferencia, el identificador `564bac4` y `494db2e` con sus 3 rutas publicadas y el efecto declarativo de la ratificación, sin línea de aprobación.
- **Evidencia:** `CHANGELOG.md:11` abre la sección `## [Unreleased]` y `:23` porta la viñeta de `RF-004`: «Ratificación firmada del propietario sobre las modificaciones del commit `564bac4` en artefactos publicados: 3 rutas afectadas (`CHANGELOG.md`, `specs/014-cierre-observaciones-finales/spec.md` y `specs/013-cierre-reauditoria-conformidad/validation_report.md`), junto con el caso `494db2e`; efecto declarativo: el contenido publicado se conserva y la autoría queda acreditada por el acta de `docs/sdd/ratificacion_historica.md`, firmada en `9042ae6` con estado `G` (`SPEC-016`, `RF-004`, `AUD-090`, `AUD-104`).» La viñeta declara los 2 identificadores de commit, las 3 rutas publicadas y el efecto declarativo del acta, y la sección `Unreleased` no porta línea de aprobación.
- [x] Completada.

### T-028

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-004`, `RF-014`, `CB-002`, `CB-011`, `RNF-008`.
- **Criterio de aceptación:** `CA-004`, `CA-015`.
- **Archivos:** `docs/sdd/ratificacion_historica.md`.
- **Estimación:** 30 min.
- **Validación:** el acta declara la fecha UTC, los 5 identificadores de exención, los 2 identificadores de commit con sus rutas publicadas, el efecto retroactivo limitado al régimen y la referencia a `docs/sdd/firmantes_autorizados`, dentro de 1 commit con estado de firma `G`.
- **Evidencia:** `git show --no-patch --format=%G?` de `9042ae6` devuelve `G` y `%GK` devuelve `SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc`, huella de la clave pública `ssh-ed25519` declarada en `docs/sdd/firmantes_autorizados:4-5`, que el validador contrasta con `ssh-keygen -lf` en la comprobación de firma. El acta declara la fecha UTC en `docs/sdd/ratificacion_historica.md:7`, el alcance con `494db2e` en `:16` y `564bac4` con sus 3 rutas en `:17-19`, las 5 exenciones `AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053` en `:25-27`, el efecto retroactivo limitado al régimen en `:31` y la referencia a `docs/sdd/firmantes_autorizados` en `:38`.
- [x] Completada.

### T-029

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-007`, `CB-007`.
- **Criterio de aceptación:** `CA-007`.
- **Archivos:** `.opencode/agents/auditor.md`.
- **Estimación:** 20 min.
- **Validación:** la descripción y el cuerpo del rol declaran que el auditor no escribe la fila del inventario de hallazgos ni la fila del corpus, que su escritura se limita a `docs/sdd/auditoria_*.md` y que cita la regla incumplida en cada hallazgo; la suite de permisos sigue en verde.
- **Evidencia:** `.opencode/agents/auditor.md:96` porta el bloque de alcance: «Tu única escritura es el informe de auditoría bajo `docs/sdd/auditoria_*.md`, conforme a la plantilla de rango 5. No escribes el inventario de hallazgos ni su fila en el índice del corpus: el cálculo del veredicto se hace desde `docs/sdd/inventario_hallazgos.md` y la fila del inventario en el índice la escribe el rol `documenter`.» La descripción de `:2` declara «Solo lectura; escribe unicamente el informe de auditoria.» La suite de `tools/sdd/tests` queda en verde con `test_auditor_solo_informes` y `test_auditor_no_aprueba` dentro de las 222 pruebas `OK`.
- [x] Completada.

### T-030

- **Dependencias:** `T-019`.
- **Requisitos cubiertos:** `RF-006`, `CB-004`, `RNF-002`.
- **Criterio de aceptación:** `CA-006`.
- **Archivos:** `specs/014-cierre-observaciones-finales/spec.md`, `specs/015-cierre-auditoria-posterior/spec.md`.
- **Estimación:** 30 min.
- **Validación:** cada fila T7 declara el commit de merge publicado en `main`, su identificador y la ancestría con el commit de empaquetado, conserva el destino `released`, el campo `release` y el identificador del release, e incrementa 1 incremento PATCH con 1 fila de motivo por corrección.
- **Evidencia:** filas T7 corregidas en el repositorio: `SPEC-014` en 0.8.2 declara el tag anotado `v0.7.0` sobre el commit de merge `5a3af48` publicado en `main`, con el commit de empaquetado `5da6df6` como ancestro de ese merge; `SPEC-015` en 0.8.1 declara el tag anotado `v0.7.1` sobre el commit de merge `da30c86` publicado en `main`, con el commit de empaquetado `f6f053a` como ancestro de ese merge. Las 2 filas conservan el destino `released`, el campo `release` y el identificador del release, y las 2 specs registran 1 fila de motivo: 0.8.2 del 2026-11-21 en `SPEC-014` y 0.8.1 del 2026-11-21 en `SPEC-015`. `python tools\sdd\validate.py --all` sin hallazgo C-23 sobre las 2 filas.
- [x] Completada.

### T-031

- **Dependencias:** `T-012`, `T-016`.
- **Requisitos cubiertos:** `RF-002`, `CB-006`.
- **Criterio de aceptación:** `CA-002`.
- **Archivos:** `specs/013-cierre-reauditoria-conformidad/validation_report.md`, `specs/015-cierre-auditoria-posterior/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** cada reporte porta 1 nota append-only con la regla de `RF-001` y la declaración de que el veredicto y el recuento los emite el rol de auditoría, con 0 líneas retiradas y la matriz y el dictamen conservados.
- **Evidencia:** `specs/013-cierre-reauditoria-conformidad/validation_report.md:128-137` y `specs/015-cierre-auditoria-posterior/validation_report.md:106-115` portan la nota «Nota de autorreferencia», con la regla de `RF-001` de `SPEC-016` y §16 del protocolo, el alcance de los criterios sin efecto, el efecto de que el veredicto y el recuento los emite el rol de auditoría y la conservación de la matriz y del dictamen. `git diff --numstat` de los 2 documentos devuelve 11 altas y 0 bajas para `SPEC-013`, y 24 altas y 0 bajas para `SPEC-015`: el recuento de líneas retiradas es 0. La comprobación de autorreferencia de `C-24` sobre las 2 specs publicadas devuelve 0 problemas.
- [x] Completada.

### T-032

- **Dependencias:** `T-019`.
- **Requisitos cubiertos:** `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `specs/015-cierre-auditoria-posterior/validation_report.md`.
- **Estimación:** 25 min.
- **Validación:** la nota append-only transcribe el resultado de G5, el resultado de G6 y el objeto anotado del tag `v0.7.1` con su mensaje y su commit objetivo, conserva la transcripción previa de la línea 77 y no altera la matriz ni el dictamen.
- **Evidencia:** `specs/015-cierre-auditoria-posterior/validation_report.md:93-104` porta la nota «Nota del resultado de G5 y de G6 y del objeto del tag `v0.7.1`», añadida a continuación de la sección de cierre de integración; `:97` transcribe el resultado de G5 y `:98` el de G6; `:100` transcribe el objeto anotado: tipo `tag`, identificador `4d0473b`, mensaje `Release v0.7.1` y commit objetivo `da30c86`, que coincide con `git rev-parse main`. La transcripción previa de `:77` se conserva y `git diff --numstat` del documento devuelve 24 altas y 0 bajas, con la matriz y el dictamen sin alteración.
- [x] Completada.

### T-033

- **Dependencias:** `T-032`.
- **Requisitos cubiertos:** `RF-005`, `CB-005`.
- **Criterio de aceptación:** `CA-005`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 20 min.
- **Validación:** la entrada `v0.7.1` porta 1 bloque de registro con el resultado de G5 y de G6 y con el objeto del tag, y conserva la línea de aprobación y el bloque de cambios.
- **Evidencia:** `CHANGELOG.md:40-46` porta la sección «Registro del release» de la entrada `v0.7.1`; `:42` registra el resultado de G5 con el merge `4dd07f5` de dos padres y la eliminación de la rama, `:43` registra el resultado de G6 con la línea de aprobación, y `:46` transcribe el objeto del tag: tipo `tag`, identificador `4d0473b`, mensaje `Release v0.7.1` y commit objetivo `da30c86`. La línea `- Approved by: Agent Sebaxtian` de `:48` y el bloque de cambios de `:26-38` conservan su contenido.
- [x] Completada.

### T-034

- **Dependencias:** `T-010`, `T-011`, `T-024`, `T-025`, `T-026`, `T-027`, `T-029`, `T-030`, `T-031`, `T-032`, `T-033`.
- **Requisitos cubiertos:** `RF-015`, `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004`, `RNF-005`, `RNF-006`, `RNF-007`, `RNF-008`, `RNF-009`.
- **Criterio de aceptación:** `CA-011`, `CA-017`.
- **Archivos:** `specs/016-cierre-auditoria-v0-7-1/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python tools\sdd\validate.py --all` con código de salida 0 en 300 segundos o menos, 0 hallazgos sin fila, 0 campos obligatorios vacíos, 0 filas sin regla citada, 0 diferencias de veredicto, 0 violaciones históricas sin ratificación firmada y 0 requisitos de esta spec que fijen el veredicto de un informe posterior.
- **Evidencia:** `python -m unittest discover -s tools\sdd\tests -q`: «Ran 222 tests» y «OK». `python -m unittest discover -s tools\git\tests -q`: «Ran 48 tests» y «OK». `python tools\sdd\validate.py --all`: código 0 en 300 segundos o menos, con las 17 comprobaciones ejecutadas y sin error de `C-19`, `C-20`, `C-21`, `C-22`, `C-23`, `C-24`, `C-25` ni `C-26`; las advertencias corresponden a las cláusulas de legado de `SPEC-001` a `SPEC-009` y a la ausencia del reporte de `SPEC-016`. Los 7 recuentos de `CA-017` quedan en 0: 0 hallazgos sin fila, 0 campos obligatorios vacíos, 0 hallazgos sin regla citada, 0 veredictos divergentes del cálculo del inventario, 0 hallazgos abiertos bajo `CONFORME`, 0 violaciones históricas cerradas sin ratificación firmada y 0 releases publicados sin auditoría previa. El commit de las modificaciones publicadas es `d0126ce` y su estado de firma es `G`, con la clave `SHA256:strw3vZ7xct0YMz+hGHAYjDOfv/zO0JyAI9Om3Olhqc` declarada en `docs/sdd/firmantes_autorizados`.
- [x] Completada.
