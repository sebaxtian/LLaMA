# Tareas - SPEC-003

## Progreso

- [x] 5 de 5 tareas completadas.

Orden TDD: T-001 y T-003 escriben las pruebas en rojo. T-002 y T-004 implementan hasta el verde. T-005 es la regresión sobre reportes reales y la verificación final.

## Tareas

### T-001 - Pruebas en rojo: dictamen, matriz y ausencia de reporte

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-005`, `CB-001`, `CB-002`, `CB-004`, `RNF-002`.
- **Criterios cubiertos:** `CA-001`, `CA-002`, `CA-003`, `CA-005`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/g4/**`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests`. Salida esperada: código `1`. Fallan en rojo las pruebas de `no-convergido-marcado`, `convergido-sin-marcar`, `fila-fallado`, `sin-reporte-tasked` con G4 y `sin-reporte-validated` sin compuerta. Pasan `dictamen-ok`, `prosa-no-converge`, `fila-no-pasado`, `sin-reporte-draft`, `sin-reporte-tasked` sin compuerta y la guarda de RNF-002.
- **Evidencia:**
  - Pruebas nuevas: 11 (`TestDictamenG4` 4, `TestMatrizG4` 2, `TestReporteAusente` 4, `TestDependencias` 1). Fixtures nuevos: 10 carpetas en `tools/sdd/tests/fixtures/g4/`.
  - Ejecución: `python -m unittest discover -s tools\sdd\tests` → `Ran 24 tests`, `FAILED (failures=5)`, código de salida `1`. Línea base previa: 13 pruebas en verde.
  - Fallan por aserción (no por import ni sintaxis): `no-convergido-marcado`, `convergido-sin-marcar`, `fila-fallado`, `sin-reporte-tasked` con G4, `sin-reporte-validated` sin compuerta.
  - Pasan: `dictamen-ok`, `prosa-no-converge`, `fila-no-pasado`, `sin-reporte-draft`, `sin-reporte-tasked` sin compuerta, guarda RNF-002.
  - Método: las pruebas de integración llaman a `main --spec SPEC-001 [--gate G4]` con `list_spec_dirs` y `validate_global` parcheados, y capturan el `v.Reporter`. No dependen de la firma nueva de `validate_report`.
  - `tools/sdd/validate.py` sin modificar.
- [x] Completada.

### T-002 - Implementación verde: dictamen, matriz y ausencia de reporte

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-005`, `CB-001`, `CB-002`, `CB-004`.
- **Criterios cubiertos:** `CA-001`, `CA-002`, `CA-003`, `CA-005`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` con código `0`, y `python tools\sdd\validate.py --spec SPEC-001 --gate G4` con código `0`. Implementa DEC-001, DEC-002 y DEC-003.
- **Evidencia:**
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 24 tests ... OK`, código `0` (0 fallos; antes 5 fallos).
  - `python tools\sdd\validate.py --all` → `[WARN] specs\003-validacion-g4\validation_report.md: validation_report.md no existe`, código `0`. SPEC-001 y SPEC-002 sin hallazgos.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4` → `OK: sin hallazgos.`, código `0`.
  - `python tools\sdd\validate.py --spec SPEC-002 --gate G4` → `OK: sin hallazgos.`, código `0`.
  - `python tools\sdd\validate.py --spec SPEC-003 --gate G4` → `[ERROR] specs\003-validacion-g4\validation_report.md: validation_report.md ausente (obligatorio con G4/G5/G6 o en estado validated/released)`, código `1`. Es el comportamiento exigido por RF-001: SPEC-003 aún no tiene reporte de validación porque está en `tasked`. No es un fallo de implementación.
  - `git diff --check` sin salida sobre `validate.py`, tests y `tasks.md`.
  - Cambios en `validate.py`: `DICTAMEN_RE`, `FAILING_CELLS`, `GATES_REQUIRING_REPORT`, `STATES_REQUIRING_REPORT`; funciones `parse_dictamen`, `failing_rows`, `report_required`, `read_status`; `validate_report(spec_id, spec_dir, rep, gate)` y sus dos llamadas en `main`. Sin cambios en códigos de salida ni en dependencias.
- [x] Completada.

### T-003 - Pruebas en rojo: cobertura RF/CB → CA y códigos de salida

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-004`, `RNF-001`.
- **Criterios cubiertos:** `CA-004`, `CA-005`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/cobertura/**`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests`. Salida esperada: código `1`. Falla en rojo la prueba que exige una advertencia que nombre el RF no cubierto en `cobertura/faltante`. Pasan `cobertura/completa` y las pruebas de códigos `0`, `1` y `2`, que ya cumplen RNF-001 con el comportamiento vigente.
- **Evidencia:**
  - Pruebas nuevas: 10 (`TestCoberturaRF004` 3, `TestCodigosSalida` 5, `TestCoberturaReal` 2). Fixtures nuevos: `tools/sdd/tests/fixtures/cobertura/completa` y `cobertura/faltante`.
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 34 tests`, `FAILED (failures=1)`, código `1`. Línea base: 24 pruebas en verde.
  - Falla esperada, por aserción (no por import ni por API inexistente): `test_requisito_sin_cubre_genera_advertencia_que_lo_nombra`. Motivo: `AssertionError: 'RF-002' not found in set()`. No existe aún advertencia de cobertura; la implementará T-004 (DEC-004).
  - Pasan: `cobertura/completa` sin advertencias de cobertura, `cobertura/faltante` sin errores, código `0` con advertencias de cobertura, código `0` sin hallazgos, código `1` por error de validación, código `2` sin argumentos y con `SPEC-999`, SPEC-002 con G4 sin advertencias RF/CB, SPEC-001 con G4 sin errores y código `0`.
  - Decisión sobre SPEC-001 (AMB-003): no declara «Cubre:», así que sus huecos son advertencias. La prueba exige ausencia de errores y código `0`, no ausencia de advertencias. La presencia de advertencias de cobertura para SPEC-001 se verificará en T-004.
  - Método: `invoke_main` y `run_main` parchean `list_spec_dirs` y `validate_global`, y capturan `v.Reporter` mediante subclase. No se llama a funciones nuevas.
  - `tools/sdd/validate.py` sin modificar en esta tarea.
- [x] Completada.

### T-004 - Implementación verde: cobertura RF/CB → CA

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-004`, `RNF-001`.
- **Criterios cubiertos:** `CA-004`, `CA-005`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` con código `0`, y `python tools\sdd\validate.py --spec SPEC-001 --gate G2` con código `0`, que muestra advertencias de cobertura para SPEC-001 sin cambiar el código. Implementa DEC-004.
- **Evidencia:**
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 34 tests`, `OK`, código `0` (0 fallos; antes 1 fallo en `test_requisito_sin_cubre_genera_advertencia_que_lo_nombra`).
  - `python tools\sdd\validate.py --all` → código `0`, sin errores. Advertencias:
    - `[WARN] specs\001-main-menu\spec.md`: RF-001, RF-002, RF-003, RF-004, RF-005, RF-006, CB-001, CB-002 y CB-003 no aparecen en ninguna línea «Cubre:» (9 advertencias). Esperadas: SPEC-001 no declara «Cubre:» (AMB-003, CB-003).
    - `[WARN] specs\003-validacion-g4\validation_report.md: validation_report.md no existe`. Esperada: SPEC-003 está en `tasked`.
  - SPEC-002 con `--all` y con `--spec SPEC-002 --gate G4`: sin advertencias de cobertura, código `0`.
  - SPEC-001 con `--spec SPEC-001 --gate G4`: 9 advertencias de cobertura, sin errores, código `0`.
  - `--spec SPEC-003 --gate G4`: código `1` por reporte ausente (RF-001). Es el mismo comportamiento de T-002, no un fallo de cobertura.
  - Implementación: `_section` (sección de nivel 2 por título), `coverage_gaps(spec_body)` (pura: RF/CB de «Requisitos funcionales» y «Casos borde» menos los de líneas «Cubre:» de «Criterios de aceptación», sin duplicados) y una advertencia por requisito en `validate_spec`. Sin errores nuevos ni cambios en códigos de salida ni en dependencias.
  - `git diff --check` sin salida.
- [x] Completada.

### T-005 - Regresión sobre reportes reales y verificación final

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `CB-003`, `RNF-001`, `RNF-002`, `RNF-003`.
- **Criterios cubiertos:** `CA-005`.
- **Archivos:** `tools/sdd/tests/test_validate.py`.
- **Estimación:** 20 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` con código `0`, incluida la prueba de regresión sobre los reportes de SPEC-001 y SPEC-002 con G4 (sin errores). Después, `python tools\sdd\validate.py --spec SPEC-001 --gate G4`, `--spec SPEC-002 --gate G4` y `--all` con código `0`, y `git diff --check` sin salida.
- **Evidencia:**
  1. `python -m unittest discover -s tools\sdd\tests` → `Ran 34 tests`, `OK`, código `0`. Incluye la regresión sobre reportes reales: `TestCoberturaReal` valida SPEC-002 con G4 (sin advertencias RF/CB) y SPEC-001 con G4 (sin errores, código `0`).
  2. `python tools\sdd\validate.py --spec SPEC-001 --gate G4` → 9 advertencias de cobertura (RF-001 a RF-006, CB-001 a CB-003), sin errores, código `0`. Esperadas por AMB-003.
  3. `python tools\sdd\validate.py --spec SPEC-002 --gate G4 --git` → `[ERROR] git: rama actual 'feat/validacion-g4' no coincide con la declarada 'feat/orquestacion-subagentes-sdd'`, código `1`. **Limitación de la compuerta, no fallo de la tarea:** SPEC-002 declara una rama ya integrada en `dev`; `--git` solo puede pasar sobre esa rama. Sin `--git`: `python tools\sdd\validate.py --spec SPEC-002 --gate G4` → `OK: sin hallazgos.`, código `0`.
  4. `python tools\sdd\validate.py --all` → código `0`, sin errores. Advertencias: 9 de cobertura en SPEC-001 (esperadas) y 1 de reporte ausente en SPEC-003 (`tasked`, esperada).
  5. `git diff --check` → sin salida, código `0`.
  - Comprobación CB-003: `validate_report` con G4 sobre `specs/001-main-menu` y `specs/002-orquestacion-subagentes-sdd` no produce errores ni hallazgos.
  - Correcciones durante T-005: ninguna. No se modificó código en esta tarea.
  - Nota: `--spec SPEC-003 --gate G4` devuelve código `1` por reporte ausente (RF-001). Es correcto mientras SPEC-003 esté en `tasked`; el reporte corresponde a la etapa Validate.
- [x] Completada.
