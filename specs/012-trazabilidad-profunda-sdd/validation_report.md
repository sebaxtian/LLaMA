# Reporte de validación — SPEC-012

*Artefacto de rango 6 escrito por el subagente `reviewer`: audita la convergencia de `SPEC-012` sobre el commit validado y no declara compuerta. Después de G4 el documento es append-only: el registro de G5 y de G6 se añade sin alterar la matriz ni el dictamen.*

<!-- Este reporte no porta casilla ni sección de firma del propietario: el registro de G4 vive en la sección de aprobaciones de `spec.md`. -->

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/trazabilidad-profunda-sdd`.
- Commit validado: `a3a2794` («docs(sdd): cerrar la implementacion y verificar G3 de SPEC-012»).
- Estado de la spec: `implemented`, versión 0.6.0, con 9 requisitos funcionales, 8 requisitos no funcionales, 18 casos borde y 17 criterios de aceptación.
- Herramientas: Python 3 con la biblioteca estándar (`unittest`), Git en Windows y el validador determinista `tools/sdd/validate.py`.
- Suite completa: `python -m unittest discover -s tools\sdd\tests -q` devuelve `Ran 131 tests in 1.247s` y `OK`, con 111 pruebas vigentes y 20 nuevas.
- Ejecución agregada: `python tools\sdd\validate.py --all` devuelve código 0 en dos ejecuciones consecutivas con este reporte en disco, sin entradas `[ERROR]` y con 60 advertencias de cláusula de legado en las dos salidas.
- Ejecución de la spec: `python tools\sdd\validate.py --spec SPEC-012` devuelve código 0 sin entradas `[ERROR]`.
- Árbol de trabajo sobre `a3a2794`: `specs/012-trazabilidad-profunda-sdd/spec.md` y `specs/INDEX.md` conservan la transición a `implemented` sin commitear, y este reporte es el artefacto de la etapa 7.
- Los recuentos por clase de prueba (`Ran 5 tests`, `Ran 4 tests`, `Ran 3 tests`) se contrastan con el registro de `T-001` a `T-005` y con la diferencia 131 − 111 = 20 pruebas nuevas; la sesión ejecutó la suite en agregado.

## Matriz de trazabilidad

| Requisito | CA | Prueba o comando | Evidencia | Estado |
|---|---|---|---|---|
| `RF-001` | `CA-001` | `python -m unittest tools.sdd.tests.test_validate.TestEnlaceCriterioTarea` | `Ran 5 tests` y `OK`; `test_enlace_ca_tarea` devuelve código 0 sobre `enlace/valido` y `test_formato_de_varios_ca` exige código 1 con `T-001` y «coma» | PASADO |
| `RF-002` | `CA-001`, `CA-003` | `TestEnlaceCriterioTarea.test_ca_inexistente_en_tarea` y `test_ca_de_otra_spec` | código 1 con `T-001` y `CA-099`; código 1 con `T-001` y `SPEC-011` como spec de destino | PASADO |
| `RF-003` | `CA-002` | `TestEnlaceCriterioTarea.test_ca_sin_tarea` | código 1 con el identificador `CA-003` del criterio que ninguna tarea declara | PASADO |
| `RF-004` | `CA-004` | `python -m unittest tools.sdd.tests.test_validate.TestEvidenciaDeTarea` | `Ran 4 tests` y `OK`; `test_evidencia_corta` y `test_evidencia_con_marcador` devuelven código 1 con `T-001`; `test_tarea_abierta_sin_evidencia` devuelve código 0 y su control con la casilla marcada devuelve código 1 | PASADO |
| `RF-005` | `CA-005`, `CA-006` | `TestReferenciaDeCommit.test_commit_con_spec`, `test_commit_sin_spec` y `python tools\sdd\validate.py --all` | `Ran 4 tests` y `OK`; `test_commit_sin_spec` devuelve código 1 con el sha abreviado `bbbbbbb`; `--all` no emite hallazgo `C-16` y su bloque de alcance declara «historial de commits y cadena «Spec: SPEC-NNN»» | PASADO |
| `RF-006` | `CA-007`, `CA-008` | `python -m unittest tools.sdd.tests.test_validate.TestCierreDeIntegracion` y `python tools\sdd\validate.py --all` | `Ran 4 tests` y `OK`; los siete reportes declaran `## Cierre de integración` con `Merge:` y `Release:`; `--all` no emite hallazgo `C-17` en `SPEC-001` a `SPEC-007` | PASADO |
| `RF-007` | `CA-009`, `CA-010` | `git diff --numstat dev...HEAD -- specs` y `python tools\sdd\validate.py --spec SPEC-001` hasta `--spec SPEC-007` | 48 tareas con `Criterio de aceptación` y `Evidencia` (4, 10, 5, 5, 9, 5 y 10); siete versiones con la fila «Regularización de la trazabilidad de tareas y del cierre de integración»; 35 líneas añadidas y 0 eliminadas en los siete reportes; 0 hallazgos `C-14`, `C-15` y `C-18` en las siete specs | PASADO |
| `RF-008` | `CA-011` | `git diff dev...HEAD -- specs` y `python tools\sdd\validate.py --all` | 0 líneas añadidas o eliminadas en el historial de transiciones de las siete specs; siete advertencias `C-07` por la subsección ausente, sin `[ERROR]` | PASADO |
| `RF-009` | `CA-012` | `TestVersionadoDeLaRegularizacion.test_legado_de_008_a_011` y `python tools\sdd\validate.py --all` | `Ran 3 tests` y `OK`; advertencia con código 0 en `SPEC-010` y error con código 1 en `SPEC-012`; `TRACE_LEGACY_WINDOW = set(TRACE_LEGACY_SPECS)` en `tools/sdd/validate.py` líneas 149 a 153; 60 advertencias de legado y 0 errores en `--all` | PASADO |
| `RNF-001` | `CA-015` | `python tools\sdd\validate.py --all` con tiempo medido | código 0; el registro de `T-017` consigna 0,74 s y esta revisión ejecutó el comando dos veces con código 0, por debajo del umbral de 300 s | PASADO |
| `RNF-002` | `CA-016` | `TestDependencias.test_solo_biblioteca_estandar` y `python tools\sdd\validate.py --all` | `external == []`, con el mensaje de aserción «importaciones no estándar»; la ejecución agregada completa sin acceso a red ni credencial | PASADO |
| `RNF-003` | `CA-016` | `python -m unittest tools.sdd.tests.test_validate.TestCodigosSalida` | cinco pruebas: `test_codigo_0_sin_hallazgos`, `test_codigo_0_con_advertencias_de_cobertura`, `test_codigo_1_error_de_validacion`, `test_codigo_2_error_de_uso_sin_argumentos` y `test_codigo_2_spec_inexistente`; `--all` devuelve código 0 | PASADO |
| `RNF-004` | `CA-010` | `git diff dev...HEAD -- specs/001-main-menu/spec.md` hasta `specs/007-branch-protection/spec.md` | entre 3 y 4 líneas añadidas y entre 2 y 3 eliminadas por spec, limitadas a `version`, `updated` y la fila de motivo; 0 líneas de requisito, requisito no funcional, caso borde o criterio modificadas | PASADO |
| `RNF-005` | `CA-017` | `python -m unittest discover -s tools\sdd\tests -q` y recuento de las clases nuevas | `Ran 131 tests` y `OK`; 20 pruebas nuevas: `TestEnlaceCriterioTarea` 5, `TestEvidenciaDeTarea` 4, `TestReferenciaDeCommit` 4, `TestCierreDeIntegracion` 4 y `TestVersionadoDeLaRegularizacion` 3; cada clase declara el caso positivo y su control negativo con código 1 | PASADO |
| `RNF-006` | `CA-012` | `TRACE_LEGACY_SPECS` y `python tools\sdd\validate.py --all` | `TRACE_LEGACY_SPECS = {f"SPEC-{n:03d}" for n in range(8, 12)}` limita la degradación a cuatro specs; las advertencias de trazabilidad se emiten solo en `SPEC-008` a `SPEC-011` | PASADO |
| `RNF-007` | `CA-015` | dos ejecuciones consecutivas de `python tools\sdd\validate.py --all` sobre `a3a2794` con este reporte en disco | las dos salidas presentan las mismas 60 advertencias y 0 entradas `[ERROR]`, con 0 diferencias entre ambas | PASADO |
| `RNF-008` | `CA-004` | `EVIDENCE_MIN_LENGTH` y `TestEvidenciaDeTarea.test_evidencia_corta` | `EVIDENCE_MIN_LENGTH = 20` en `tools/sdd/validate.py` línea 157; 19 caracteres tras eliminar espacios produce código 1 y una transcripción de 20 o más no produce hallazgo | PASADO |
| `CB-001` | `CA-001` | `TestEnlaceCriterioTarea.test_ca_inexistente_en_tarea` | código 1 con `T-001` y `CA-099`; la casilla de la tarea no altera el resultado de la validación | PASADO |
| `CB-002` | `CA-002` | `TestEnlaceCriterioTarea.test_ca_sin_tarea` | código 1 con el identificador `CA-003` y la spec conserva su estado con la brecha declarada | PASADO |
| `CB-003` | `CA-003` | `TestEnlaceCriterioTarea.test_ca_de_otra_spec` | código 1 con `T-001` y el identificador `SPEC-011` de la spec de destino | PASADO |
| `CB-004` | `CA-004` | `TestEvidenciaDeTarea.test_evidencia_con_marcador` y `test_evidencia_corta` | código 1 con `T-001` en las dos pruebas, para la marca de pendiente y para 19 caracteres tras eliminar espacios | PASADO |
| `CB-005` | `CA-005` | `TestReferenciaDeCommit.test_commit_sin_spec` | código 1 y el error nombra el commit abreviado `bbbbbbb` | PASADO |
| `CB-006` | `CA-006` | `TestReferenciaDeCommit.test_sin_commit_de_implementacion` | la salida contiene «no aplicable» y el código de salida es 0 | PASADO |
| `CB-007` | `CA-007` | `TestCierreDeIntegracion.test_cierre_ausente` | código 1 con `SPEC-012` y el término «cierre» para una spec en estado `validated` | PASADO |
| `CB-008` | `CA-007` | `TestCierreDeIntegracion.test_cierre_sin_release` | código 1 con `SPEC-012` y el término «release» para una spec en estado `released` | PASADO |
| `CB-009` | `CA-008` | `TestCierreDeIntegracion.test_tag_divergente` | código 1 con los dos valores en conflicto `v1.1.1` y `v1.2.0` | PASADO |
| `CB-010` | `CA-012` | `TestVersionadoDeLaRegularizacion.test_legado_de_008_a_011` | advertencia con código 0 en `SPEC-010` y error con código 1 en `SPEC-012` para la misma falta de trazabilidad | PASADO |
| `CB-011` | `CA-013` | `git diff dev...HEAD --` los siete `spec.md` y `plan.md` § «Contrato de la regularización histórica» | 0 líneas de requisito, requisito no funcional o criterio modificadas; la condición de parada no se activó en ninguna de las siete specs y no hubo dependencia nueva que registrar | PASADO |
| `CB-012` | `CA-014` | `TestCierreDeIntegracion.test_cierre_completo` y `git diff --numstat dev...HEAD --` los siete `validation_report.md` | código 0 con la sección completa; 35 líneas añadidas y 0 eliminadas, de modo que la matriz y el dictamen de los siete reportes quedan sin alteración | PASADO |
| `CB-013` | `CA-009` | `git diff dev...HEAD --` los siete `tasks.md` | 8, 20, 10, 10, 16, 10 y 20 líneas añadidas: el campo `Evidencia` se incorpora sin alterar dependencias, requisitos cubiertos, archivos ni estimación | PASADO |
| `CB-014` | `CA-011` | `python tools\sdd\validate.py --all` | siete advertencias «falta la subsección «Historial de transiciones» en «## Historial de cambios» (cláusula de legado)» sin `[ERROR]`, y 0 filas de transición añadidas | PASADO |
| `CB-015` | `CA-001` | `TestEnlaceCriterioTarea.test_formato_de_varios_ca` | código 1 con `T-001` y el término «coma» para dos identificadores sin separador | PASADO |
| `CB-016` | `CA-007` | `TestCierreDeIntegracion.test_cierre_ausente` | código 1 con `SPEC-012` por la ausencia de la sección de cierre en estado `validated` | PASADO |
| `CB-017` | `CA-010` | `TestVersionadoDeLaRegularizacion.test_regularizacion_sin_patch` | código 1 con `SPEC-001` y el término «version»; la variante sin fila de motivo también devuelve código 1 con `SPEC-001` | PASADO |
| `CB-018` | `CA-006` | `TestReferenciaDeCommit.test_alcance_de_commits` | código 0 y el registro del stub contiene la llamada `merge-base`, de modo que el commit anterior al punto de integración no se examina | PASADO |

Las 35 filas se corresponden con 9 requisitos funcionales, 8 requisitos no funcionales y 18 casos borde. El único valor que converge es `PASADO`; cualquier otro valor abre una brecha en la sección siguiente.

## Brechas

Sin brechas abiertas: las 35 filas de la matriz figuran en `PASADO` y las dos ejecuciones del validador devuelven código 0 sin entradas `[ERROR]`.

### Notas de desviaciones con tratamiento

- **Disparador declarativo de `C-18`.** La comprobación solo emite hallazgo cuando la spec declara una fila de regularización o pertenece a `REGULARIZED_SPECS`; por eso no produce hallazgo en `--spec SPEC-010` ni en `--spec SPEC-012`, y la rama de error se acredita con `test_regularizacion_sin_patch` sobre la fixture de `SPEC-001` y la de advertencia con `test_legado_de_008_a_011`. Desviación declarada en la evidencia de `T-008`; no deja fila sin cobertura.
- **Etiquetas de evidencia heredadas conservadas en `SPEC-003`, `SPEC-004`, `SPEC-005` y `SPEC-007`.** La regularización conservó el texto previo de cada etiqueta `Evidencia` y añadió la transcripción de la fuente, de modo que el conteo de líneas eliminadas corresponde al reemplazo de la etiqueta vacía y no a una reescritura de contenido funcional, como exige `CB-013`.
- **Duplicación de la etiqueta `Criterios cubiertos` en `SPEC-003`.** Las cinco tareas portan ahora `Criterio de aceptación` junto a la etiqueta no canónica previa, con listas coincidentes en cada tarea; la regularización no elimina un campo publicado y `C-14` lee el campo canónico sin ambigüedad.
- **Asignación por contenido en `SPEC-007` `T-010`.** La evidencia de esa tarea se asignó por el contenido del reporte de `SPEC-007` (filas `RNF-001` a `RNF-007`) y no por una fila literal de la tarea; el texto transcrito nombra las filas de la matriz que la acreditan.
- **`SPEC-001` pasó de 0.1.0 a 0.3.1 y no a 0.1.1.** El historial de cambios de esa spec ya declaraba las filas 0.2.0 y 0.3.0 mientras el frontmatter conservaba 0.1.0; la regularización alinea el campo con su historial e incrementa la posición PATCH, de modo que `CB-017` se satisface y `C-18` no registra hallazgo. La tabla del plan preveía 0.1.1 y el valor aplicado difiere en la posición MINOR.
- **`CB-012` no se ejercitó sobre un reporte real con dictamen no convergido.** Los siete reportes publicados declaran `CONVERGIDO`; el caso se acredita por la propiedad append-only del registro (35 líneas añadidas y 0 eliminadas en los siete reportes) y por la lectura sin escritura de `check_integration_close` en `tools/sdd/validate.py`.
- **Ubicación de la sección de cierre en el reporte de `SPEC-001`.** La sección quedó después del dictamen y antes de la sección `## Aprobación` heredada, y no al final del archivo; `RF-006` exige la sección y sus líneas, y no fija la posición final.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos y casos borde con evidencia PASADO).
- [ ] NO CONVERGIDO.

> El dictamen `CONVERGIDO` indica que la matriz cumple el 100 % de requisitos y casos borde con evidencia `PASADO`. No aprueba G4: la aprobación corresponde al propietario y su registro vive en la sección de aprobaciones de `spec.md`.

## Cierre de integración

Merge: b87e32c
Release:

- G5: merge b87e32c con dos padres; validación posterior a la integración sin hallazgos; rama feat/trazabilidad-profunda-sdd eliminada en local y en remoto.
