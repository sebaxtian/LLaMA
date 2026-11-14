# Tareas — SPEC-012

*Artefacto de rango 6: descomposición de `SPEC-012` en dieciocho tareas atómicas con los ocho campos de la plantilla, dependencias acíclicas y cobertura completa de los requisitos y de los casos borde.*

## Regla de ejecución

La etapa modifica el validador determinista, su suite de pruebas y siete specs publicadas. Se ejecuta con dos escritores y una revisión:

1. El rol `coder` escribe `tools/sdd/validate.py` y `tools/sdd/tests/`, y cierra sus tareas en este archivo.
2. El `planner` escribe la regularización de tareas de `specs/001-main-menu/` a `specs/007-branch-protection/` y los artefactos de esta spec, salvo los reportes de validación.
3. El `reviewer` escribe la sección de cierre de los siete reportes publicados: su matriz de permisos le concede `specs/*/validation_report.md` y el `planner` tiene esa ruta denegada.
4. El orquestador verifica G2, G3 y G5, ejecuta el validador y la suite, y no escribe artefactos de la regularización.
5. Las validaciones que requieren shell las ejecuta la sesión orquestadora y su salida literal se transcribe en el campo `Evidencia` de la tarea.
6. Una casilla se marca solo cuando la validación de la tarea se cumple. Una validación fallida obliga a corregir el archivo y a repetir la comprobación antes del registro.
7. Cada tarea de prueba se escribe en rojo antes de la tarea de implementación que la satisface; una tarea de prueba declara su caso positivo y su caso negativo.
8. La evidencia histórica se transcribe desde el reporte de validación existente o desde el informe de auditoría, con la referencia de la fila o de la línea. Una tarea cuya evidencia no se acredite con una fuente se registra como brecha y no se redacta evidencia sin respaldo.
9. La etapa no modifica la base normativa, las plantillas de rango 5, `src/`, `models/` ni `bin/`. Una necesidad de cambio en esas rutas se registra como dependencia y no se ejecuta.

## Referencias

- `spec.md`: `SPEC-012`, versión 0.3.0, estado `planned`, compuerta G1 aprobada por `Agent Sebaxtian` en el commit firmado `cfb576b` (2026-11-14).
- `clarify.md`: cerrado con `AMB-001` a `AMB-008` resueltos, cuatro casos borde nuevos y once parches aplicados a `spec.md`.
- `plan.md`: arquitectura de seis capas, procedimientos de las comprobaciones `C-14` a `C-18`, contratos de tarea, evidencia, cierre de integración y regularización, diez decisiones `DEC-001` a `DEC-010` y matriz de cobertura de treinta y cinco filas.
- `docs/sdd/plantillas/tasks.md`: plantilla aplicada, con los ocho campos por tarea.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §4 ciclo de siete etapas, §7 trazabilidad, §9 versionado, §12 roles y permisos y §14 contrato del validador.
- `docs/sdd/auditoria_cumplimiento_sdd.md`: bloque B4, hallazgos `AUD-022`, `AUD-041`, `AUD-042`, `AUD-043`, `AUD-044` y `AUD-072`, y tabla de integración y release de la sección 6.

## Progreso

- [ ] 16 de 18 tareas completadas.

## Archivos de la etapa y escritor

| # | Archivo o ruta | Tareas | Escritor |
|---|---|---|---|
| 1 | `tools/sdd/tests/test_validate.py` y `tools/sdd/tests/fixtures/trazabilidad/` | `T-001` a `T-005` | `coder` |
| 2 | `tools/sdd/validate.py` | `T-006`, `T-007` y `T-008` | `coder` |
| 3 | `specs/001-main-menu/tasks.md` | `T-009` | `planner` |
| 4 | `specs/002-orquestacion-subagentes-sdd/tasks.md` | `T-010` | `planner` |
| 5 | `specs/003-validacion-g4/tasks.md` | `T-011` | `planner` |
| 6 | `specs/004-editor-documentacion/tasks.md` | `T-012` | `planner` |
| 7 | `specs/005-compuertas-completas/tasks.md` | `T-013` | `planner` |
| 8 | `specs/006-observaciones-cierre/tasks.md` | `T-014` | `planner` |
| 9 | `specs/007-branch-protection/tasks.md` | `T-015` | `planner` |
| 10 | Los siete `validation_report.md` publicados | `T-016` | `reviewer` |
| 11 | `specs/012-trazabilidad-profunda-sdd/tasks.md` | cierre de cada tarea, `T-017` y `T-018` | `coder` para las casillas y `planner` para el cierre |

`T-017` y `T-018` son tareas de verificación y de cierre: no producen archivos fuera de `tasks.md`.

## Orden de ejecución y dependencias

- Grupo 1 (pruebas en rojo): `T-001` sin dependencias; `T-002` depende de `T-001`; `T-003` depende de `T-002`; `T-004` depende de `T-003`; `T-005` depende de `T-004`.
- Grupo 2 (implementación mínima): `T-006` depende de `T-001`; `T-007` depende de `T-003` y de `T-004`; `T-008` depende de `T-005`.
- Grupo 3 (regularización): `T-009` depende de `T-006`, `T-007` y `T-008`; `T-010` depende de `T-009`; `T-011` depende de `T-010`; `T-012` depende de `T-011`; `T-013` depende de `T-012`; `T-014` depende de `T-013`; `T-015` depende de `T-014`; `T-016` depende de `T-015`.
- Grupo 4 (verificación y cierre): `T-017` depende de `T-016`; `T-018` depende de `T-017`.

El grafo es acíclico y cada arista apunta a una tarea existente de este archivo.

## Tareas

### T-001: Pruebas del enlace criterio y tarea

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `CB-001`, `CB-002`, `CB-003`, `CB-015`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-003`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/trazabilidad/enlace/`.
- **Estimación:** 30 min.
- **Validación:** cinco pruebas nuevas en rojo: `test_enlace_ca_tarea` con una tarea que declara un criterio existente y salida 0; `test_ca_inexistente_en_tarea` con código 1 y el identificador de la tarea; `test_ca_sin_tarea` con código 1 y el identificador del criterio; `test_ca_de_otra_spec` con código 1 y la spec de destino; `test_formato_de_varios_ca` con dos identificadores sin coma y código 1.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestEnlaceCriterioTarea` devuelve `Ran 5 tests` y `OK`; las cinco pruebas se escribieron en rojo en el lote A y pasan tras `T-006`.
- [x] Completada.

### T-002: Pruebas del criterio de evidencia

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-004`, `RNF-008`, `CB-004`.
- **Criterio de aceptación:** `CA-004`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/trazabilidad/evidencia/`.
- **Estimación:** 25 min.
- **Validación:** cuatro pruebas nuevas en rojo: `test_evidencia_valida` con 20 caracteres o más y salida 0; `test_evidencia_corta` con 19 caracteres y código 1; `test_evidencia_con_marcador` con el campo sin sustituir y código 1; `test_tarea_abierta_sin_evidencia` con la casilla sin marcar y salida 0.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestEvidenciaDeTarea` devuelve `Ran 4 tests` y `OK`; la prueba corta, la del marcador sin sustituir y la de la tarea abierta se escribieron en rojo en el lote A y pasan tras `T-006`.
- [x] Completada.

### T-003: Pruebas de la referencia del commit

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-005`, `CB-005`, `CB-006`, `CB-018`.
- **Criterio de aceptación:** `CA-005`, `CA-006`, `CA-016`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/trazabilidad/commits/`.
- **Estimación:** 30 min.
- **Validación:** cuatro pruebas nuevas en rojo: `test_commit_con_spec` con la cadena `Spec: SPEC-012` y salida 0; `test_commit_sin_spec` con código 1 y el identificador abreviado del commit; `test_alcance_de_commits` con un commit anterior al punto de integración y salida 0; `test_sin_commit_de_implementacion` con la comprobación informada como no aplicable y salida 0.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestReferenciaDeCommit` devuelve `Ran 4 tests` y `OK`; las cuatro pruebas se escribieron en rojo en el lote A y pasan tras `T-007`, incluida la que informa la comprobación como no aplicable sin commits de implementación.
- [x] Completada.

### T-004: Pruebas del cierre de integración

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-006`, `CB-007`, `CB-008`, `CB-009`, `CB-016`.
- **Criterio de aceptación:** `CA-007`, `CA-008`, `CA-014`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/trazabilidad/cierre/`.
- **Estimación:** 30 min.
- **Validación:** cuatro pruebas nuevas en rojo: `test_cierre_completo` con la sección y sus dos líneas, salida 0; `test_cierre_ausente` en estado `validated` sin sección, código 1; `test_cierre_sin_release` en estado `released` sin línea de release, código 1; `test_tag_divergente` con el tag distinto del frontmatter, código 1 y los dos valores en conflicto.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestCierreDeIntegracion` devuelve `Ran 4 tests` y `OK`; la ausencia de sección, de release y el tag divergente se escribieron en rojo en el lote A y pasan tras `T-007`.
- [x] Completada.

### T-005: Pruebas del versionado de la regularización y de la ventana de legado

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RNF-006`, `CB-017`.
- **Criterio de aceptación:** `CA-010`, `CA-012`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/trazabilidad/versionado/`.
- **Estimación:** 25 min.
- **Validación:** tres pruebas nuevas en rojo: `test_regularizacion_patch` con incremento de la posición PATCH y fila de motivo, salida 0; `test_regularizacion_sin_patch` con la versión sin cambio, código 1; `test_legado_de_008_a_011` con una falta de trazabilidad en `SPEC-010` informada como advertencia y salida 0.
- **Evidencia:** `python -m unittest tools.sdd.tests.test_validate.TestVersionadoDeLaRegularizacion` devuelve `Ran 3 tests` y `OK`; el incremento PATCH válido, la falta de incremento como error y la degradación de `SPEC-008` a `SPEC-011` a advertencia se escribieron en rojo en el lote A y pasan tras `T-008`.
- [x] Completada.

### T-006: Implementación del enlace criterio y tarea y de la evidencia

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RNF-008`, `CB-001`, `CB-002`, `CB-003`, `CB-004`, `CB-015`.
- **Criterio de aceptación:** `CA-001`, `CA-002`, `CA-003`, `CA-004`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** las nueve pruebas de `T-001` y `T-002` en verde y `python -m unittest discover -s tools\sdd\tests -q` sin regresión sobre las 111 pruebas vigentes.
- **Evidencia:** `python -m unittest discover -s tools\sdd\tests -q` devuelve `Ran 131 tests in 1.076s` y `OK`: 111 vigentes y 20 nuevas; las nueve pruebas de `T-001` y `T-002` pasan con `check_ca_links` y `check_evidence` implementados en `tools/sdd/validate.py`.
- [x] Completada.

### T-007: Implementación de la referencia del commit y del cierre de integración

- **Dependencias:** `T-003`, `T-004`.
- **Requisitos cubiertos:** `RF-005`, `RF-006`, `CB-005`, `CB-006`, `CB-007`, `CB-008`, `CB-009`, `CB-016`, `CB-018`.
- **Criterio de aceptación:** `CA-005`, `CA-006`, `CA-007`, `CA-008`, `CA-016`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** las ocho pruebas de `T-003` y `T-004` en verde; `python tools\sdd\validate.py --all` ejecuta las comprobaciones de historial y devuelve el bloque de alcance con la comprobación declarada.
- **Evidencia:** `python tools\sdd\validate.py --all` devuelve código 0 y su bloque de alcance declara «historial de commits y cadena `Spec: SPEC-NNN`» y «cierre de integración y versionado de la regularización»; las ocho pruebas de `T-003` y `T-004` pasan con `check_commit_references` y `check_integration_close`.
- [x] Completada.

### T-008: Implementación del versionado y de la ventana de legado

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-009`, `RNF-006`, `CB-010`, `CB-017`.
- **Criterio de aceptación:** `CA-010`, `CA-012`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** las tres pruebas de `T-005` en verde; `python tools\sdd\validate.py --spec SPEC-010` informa la falta como advertencia y `python tools\sdd\validate.py --spec SPEC-012` la informa como error.
- **Evidencia:** `python tools\sdd\validate.py --all` devuelve código 0 con 44 hallazgos `C-14` y 4 `C-17`, todos en `SPEC-008` a `SPEC-011`, y `python -m unittest discover -s tools\sdd\tests -q` devuelve `Ran 131 tests` y `OK`. La ventana se endureció por decisión del propietario: `TRACE_LEGACY_WINDOW = set(TRACE_LEGACY_SPECS)` limita la degradación a `SPEC-008` a `SPEC-011` y la fixture `g3/tareas-completas` recibe criterio y evidencia. Desviación declarada: el disparador de `C-18` es declarativo y no produce hallazgo en `--spec SPEC-010` ni en `--spec SPEC-012`; la rama de error se acredita con `test_regularizacion_sin_patch` sobre la fixture de `SPEC-001` y la de advertencia con `test_legado_de_008_a_011`.
- [x] Completada.

### T-009: Regularización de las tareas de SPEC-001

- **Dependencias:** `T-006`, `T-007`, `T-008`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/001-main-menu/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** las 4 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-001` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior muestra como diferencia solo los dos campos añadidos, la versión y la fila de motivo, y 0 líneas de requisito, caso borde, criterio, estimación o estado modificadas.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-001` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/001-main-menu/tasks.md` devuelve 8 líneas añadidas y 0 eliminadas, con las 4 tareas provistas de criterio y evidencia; el frontmatter pasa de 0.1.0 a 0.3.1 con la fila «Regularización de la trazabilidad de tareas y del cierre de integración».
- [x] Completada.

### T-010: Regularización de las tareas de SPEC-002

- **Dependencias:** `T-009`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/002-orquestacion-subagentes-sdd/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** las 10 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-002` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo, con 0 líneas de contenido funcional modificadas.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-002` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/002-orquestacion-subagentes-sdd/tasks.md` devuelve 20 líneas añadidas y 0 eliminadas, con las 10 tareas provistas de criterio y evidencia; `version` pasa de 0.12.0 a 0.12.1 con la fila de regularización.
- [x] Completada.

### T-011: Regularización de las tareas de SPEC-003

- **Dependencias:** `T-010`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/003-validacion-g4/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** las 5 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-003` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-003` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/003-validacion-g4/tasks.md` devuelve 10 líneas añadidas y 5 eliminadas, limitadas a la etiqueta `Evidencia` vacía que pasa a llevar la transcripción; las 5 tareas declaran criterio y evidencia y `version` pasa de 0.6.0 a 0.6.1.
- [x] Completada.

### T-012: Regularización de las tareas de SPEC-004

- **Dependencias:** `T-011`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/004-editor-documentacion/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** las 5 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-004` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-004` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/004-editor-documentacion/tasks.md` devuelve 10 líneas añadidas y 0 eliminadas, con las 5 tareas provistas de criterio y evidencia; `version` pasa de 0.9.0 a 0.9.1.
- [x] Completada.

### T-013: Regularización de las tareas de SPEC-005

- **Dependencias:** `T-012`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/005-compuertas-completas/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** las 9 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-005` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-005` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/005-compuertas-completas/tasks.md` devuelve 16 líneas añadidas y 0 eliminadas: las 9 tareas declaran criterio, 7 reciben evidencia nueva y `T-006` y `T-007` conservan la suya; `version` pasa de 0.6.0 a 0.6.1.
- [x] Completada.

### T-014: Regularización de las tareas de SPEC-006

- **Dependencias:** `T-013`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/006-observaciones-cierre/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** las 5 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-006` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-006` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/006-observaciones-cierre/tasks.md` devuelve 10 líneas añadidas y 0 eliminadas, con las 5 tareas provistas de criterio y evidencia; `version` pasa de 0.6.0 a 0.6.1.
- [x] Completada.

### T-015: Regularización de las tareas de SPEC-007

- **Dependencias:** `T-014`.
- **Requisitos cubiertos:** `RF-007`, `RF-008`, `RNF-004`, `CB-011`, `CB-013`, `CB-014`.
- **Criterio de aceptación:** `CA-009`, `CA-011`, `CA-013`.
- **Archivos:** `specs/007-branch-protection/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** las 10 tareas declaran criterio de aceptación y evidencia con fuente; `python tools\sdd\validate.py --spec SPEC-007` no registra hallazgo de `C-14` ni de `C-15`; el contraste con la versión anterior se limita a los campos añadidos, la versión y la fila de motivo.
- **Evidencia:** `python tools\sdd\validate.py --spec SPEC-007` no registra hallazgo de `C-14`, `C-15` ni `C-18`; `git diff --numstat` de `specs/007-branch-protection/tasks.md` devuelve 20 líneas añadidas y 10 eliminadas, limitadas a la etiqueta `Evidencia` vacía que pasa a llevar la transcripción; las 10 tareas declaran criterio y evidencia, y `version` pasa de 0.2.0 a 0.2.1.
- [x] Completada.

### T-016: Regularización de los siete reportes de validación

- **Dependencias:** `T-015`.
- **Requisitos cubiertos:** `RF-006`, `RF-007`, `CB-012`.
- **Criterio de aceptación:** `CA-009`, `CA-014`.
- **Archivos:** `specs/001-main-menu/validation_report.md` a `specs/007-branch-protection/validation_report.md`.
- **Estimación:** 30 min.
- **Validación:** los siete reportes declaran la sección de cierre con el par de la tabla del plan (`753c3e5` y `v0.2.0`, `ec6a063` y `v0.3.0`, `39b27a2` y `v0.3.1`, `b38ed6c` y `v0.4.0`, `2781db5` y `v0.5.0`, `0afc2ee` y `v0.5.1`, `502c69d` y `v0.6.0`); `python tools\sdd\validate.py --spec SPEC-001` hasta `--spec SPEC-007` no registra hallazgo de `C-17`; la matriz y el dictamen de cada reporte quedan sin alteración y los siete merges se acreditan contra el historial local.
- **Evidencia:** Los siete reportes incorporan `## Cierre de integración` con `Merge:` y `Release:` de la tabla del plan y `git diff --numstat` devuelve 35 líneas añadidas y 0 eliminadas; `python tools\sdd\validate.py --all` deja 4 hallazgos de `C-17` (SPEC-008 a SPEC-011, en advertencia por legado) y ninguno en SPEC-001 a SPEC-007; los siete merges resuelven a commits de dos padres y cada tag anotado los contiene.
- [x] Completada.

### T-017: Regresión completa del corpus y de la suite

- **Dependencias:** `T-016`.
- **Requisitos cubiertos:** `RF-009`, `RNF-001`, `RNF-002`, `RNF-003`, `RNF-005`, `RNF-007`, `CB-010`, `CB-014`.
- **Criterio de aceptación:** `CA-015`, `CA-016`, `CA-017`.
- **Archivos:** `specs/012-trazabilidad-profunda-sdd/tasks.md`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests -q` devuelve 131 pruebas en verde, 111 vigentes y 20 nuevas, con una pareja positiva y negativa por comprobación; `python tools\sdd\validate.py --all` devuelve código de salida 0 dentro de 300 segundos; dos ejecuciones consecutivas sobre el mismo commit presentan 0 diferencias en el conjunto de hallazgos; `--all` ejecuta las comprobaciones de historial y `SPEC-008` a `SPEC-011` informan solo advertencia.
- **Evidencia:** Se transcribe la salida de la validación al cerrar la tarea.
- [ ] Completada.

### T-018: Cierre de alcance y traspaso al reviewer

- **Dependencias:** `T-017`.
- **Requisitos cubiertos:** `RNF-005`.
- **Criterio de aceptación:** `CA-017`.
- **Archivos:** `specs/012-trazabilidad-profunda-sdd/tasks.md`.
- **Estimación:** 20 min.
- **Validación:** las dieciocho tareas figuran cerradas con su evidencia transcrita; `python tools\sdd\validate.py --spec SPEC-012 --gate G3` devuelve código de salida 0; el paquete de traspaso reúne los cinco artefactos de la spec, las cinco comprobaciones, las veinte pruebas y la salida de la ejecución agregada, y no declara compuerta alguna.
- **Evidencia:** Se transcribe la salida de la validación al cerrar la tarea.
- [ ] Completada.
