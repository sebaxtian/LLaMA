# Tareas - SPEC-005

## Progreso

- [x] 9 de 9 tareas completadas (T-001 a T-009).

## Tareas

Orden de ejecución: una tarea por invocación de `coder` (salvo T-006, T-007 y T-008, indicadas abajo). Las pruebas de T-001 y T-003 deben fallar antes de implementar T-002 y T-004 (TDD).

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `RNF-003`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/g3/**`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests`. Las pruebas nuevas de `TestG3Tareas` (CA-001) fallan y las existentes pasan. Código `1` por las pruebas nuevas.
- **Evidencia (fase roja, 2026-11-13):**
  - Comando: `python -m unittest discover -s tools\sdd\tests -v` desde la raíz.
  - Resultado: `Ran 37 tests`, `FAILED (failures=1)`, código de salida `1`.
  - Fallo esperado: `test_tarea_pendiente_con_g3_es_error` → `AssertionError: False is not true : una tarea sin [x] con G3 debe producir error`.
  - Pasan: las 34 pruebas existentes más `test_tareas_completas_con_g3_sin_errores` y `test_sin_tareas_con_g3_es_error`. Estas dos son guardas: el validador actual ya cumple su aserción («sin tareas» ya produce error con cualquier compuerta), por lo que no pueden fallar en rojo.
  - Fixtures creados: `g3/tarea-pendiente/`, `g3/tareas-completas/`, `g3/sin-tareas/` (`spec.md` y `tasks.md`). `tools/sdd/validate.py` no se ha modificado.
- [x] Completada.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RNF-001`, `RNF-002`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` pasa (CA-001). `python tools\sdd\validate.py --spec SPEC-001 --gate G3` devuelve `0`.
- **Evidencia (fase verde G3, 2026-11-13):**
  - Cambios en `tools/sdd/validate.py`: `COMPLETED_RE`, función pura `incomplete_tasks(text) -> list[str]`, parámetro `gate` en `validate_tasks` (error por cada tarea pendiente solo si `gate == "G3"`) y `main` pasa `gate` en ambas ramas.
  - Alcance de G3 en `--all`: solo con `--gate G3` explícito, no por estado. Justificación: `plan.md` fija que la compuerta se pasa desde `main` y que el chequeo se activa «con G3». Aplicarlo por estado (`tasked`, `implementing`, `implemented`) haría fallar `--all` por SPEC-005, que está en `tasked` con tareas pendientes, y rompería el criterio de código `0`.
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 37 tests`, `OK`, código `0`.
  - `python tools\sdd\validate.py --all` → código `0`.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4` → código `0`.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G3` y `--spec SPEC-002 --gate G3` → código `0`.
  - `python tools\sdd\validate.py --spec SPEC-005 --gate G3` → código `1`, con un error por tarea pendiente T-002 a T-009. Es el comportamiento esperado hasta completar SPEC-005.
  - `git diff --check` → código `0`.
- [x] Completada.

### T-003

- **Dependencias:** `T-002`.
- **Requisitos cubiertos:** `RF-002`, `CB-001`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/matriz/**`.
- **Estimación:** 25 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests`. Fallan las pruebas nuevas de `TestMatrizEstados` para `matriz/compuesta`, `sin-columna-estado` y `celda-vacia`. Pasan `observacion` y `tabla-ajena` (CA-002).
- **Evidencia (fase roja RF-002/CB-001, 2026-11-13):**
  - Comando: `python -m unittest discover -s tools\sdd\tests -v` desde la raíz.
  - Resultado: `Ran 45 tests`, `FAILED (failures=6)`, código de salida `1`.
  - Fallos por aserción (`AssertionError: False is not true`), todos en `TestMatrizEstados`: `pendiente` (PENDIENTE), `parcial` (PARCIAL), `compuesta` («NO PASADO (2 pruebas)»), `pasado-fallado` («PASADO / FALLADO»), `sin-columna-estado` y `celda-vacia`.
  - Pasan: `observacion` («PASADO (con observación O-16)») y `tabla-ajena` («Brecha | Estado» con CERRADA). Verdes por diseño, sin error de ningún tipo.
  - Pasan las 37 pruebas existentes (45 − 6 fallos − 2 nuevas verdes = 37 sin cambios).
  - Fixtures creados: `matriz/{pendiente,parcial,compuesta,pasado-fallado,observacion,tabla-ajena,sin-columna-estado,celda-vacia}/` (`spec.md` y `validation_report.md`). `validate.py` no modificado.
  - Nota: `pendiente` y `parcial` y `pasado-fallado` no están en la lista de T-003 de `tasks.md`; se añaden por RF-002 («estado distinto de PASADO») y CA-002.
- [x] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-002`, `CB-001`, `RNF-001`.
- **Archivos:** `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` pasa (CA-002). `python tools\sdd\validate.py --spec SPEC-002 --gate G4` devuelve `0`.
- **Evidencia (fase verde RF-002/CB-001, 2026-11-13):**
  - Cambios en `tools/sdd/validate.py`: `failing_rows` y `FAILING_CELLS` sustituidos por `not_passed_rows`, `STATUS_COLUMNS`, `TRACE_FIRST_HEADERS` y `PASSED_CELL_RE` (DEC-002, DEC-003, AMB-001). `validate_report` usa `not_passed_rows`.
  - Reglas aplicadas: solo tablas cuya primera cabecera es Requisito, Criterio o CA; columna Estado o Resultado; solo filas de datos; celda superada si tras normalizar es `PASADO` con paréntesis opcional; celda vacía o sin columna de estado es error.
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 45 tests`, `OK`, código `0`.
  - `python tools\sdd\validate.py --all` → código `0`, sin errores.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4` → código `0`.
  - `python tools\sdd\validate.py --spec SPEC-002 --gate G4` → código `0`, `OK: sin hallazgos.`.
  - `python tools\sdd\validate.py --spec SPEC-003 --gate G4` → código `0`, `OK: sin hallazgos.`.
  - Comprobación de que la regla no omite datos: en los reportes reales se detectan las tablas de trazabilidad (SPEC-002 y SPEC-003 tienen 2 cada una) y ninguna fila produce entrada de error. Las tablas de verificación, sesión, brecha, caso y comando no se evalúan.
  - Ningún reporte real incumple el contrato; no se ha relajado ninguna regla.
- [x] Completada.

### T-005

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-003`, `CB-002`, `RNF-003`.
- **Archivos:** `tools/sdd/tests/test_validate.py`, `tools/sdd/tests/fixtures/rama/**`, `tools/sdd/validate.py`.
- **Estimación:** 30 min.
- **Validación:** `python -m unittest discover -s tools\sdd\tests` pasa, incluido `TestRamaEstado` (CA-003). La prueba comprueba que `git_checks` recibe `None` en `released` y `superseded`, y la rama declarada en `draft`.
- **Evidencia (RF-003/CB-002, 2026-11-13):**
  - Fase roja: `TestRamaEstado.test_released_rama_eliminada_sin_error_de_rama` falla por aserción (`AssertionError: Lists differ: [<Finding>] != []`). `test_validated_rama_distinta_sigue_siendo_error` pasa, como debe.
  - Pruebas sin Git real: `subprocess.run` se sustituye por `fake_git` (rama actual simulada).
  - Cambio en `tools/sdd/validate.py` (DEC-004): constante `NO_BRANCH_CHECK_STATES = {"released", "superseded"}`; `main` pasa la rama declarada a `git_checks` solo si el estado no está en ese conjunto.
  - Fixtures: `rama/released-rama-eliminada/` y `rama/validated-rama-distinta/` (`spec.md` y `validation_report.md`).
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 47 tests`, `OK`, código `0`.
  - `python tools\sdd\validate.py --all` → código `0`, sin errores.
  - `python tools\sdd\validate.py --spec SPEC-002 --gate G4 --git` (rama actual `feat/compuertas-completas`) → código `0`, `OK: sin hallazgos.`. Sin el cambio, SPEC-002 daría `[ERROR] git: rama actual 'feat/compuertas-completas' no coincide con la declarada 'feat/orquestacion-subagentes-sdd'` porque su estado es `released`.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4 --git` → código `0` (SPEC-001 también es `released`).
- [x] Completada.

### T-006

- **Dependencias:** `T-005`.
- **Requisitos cubiertos:** `RF-004`.
- **Archivos:** `specs/001-main-menu/spec.md`.
- **Ejecutor:** `planner`. Los permisos de `coder` impiden editar `specs/**`, salvo `tasks.md`.
- **Estimación:** 15 min.
- **Validación:** `python tools\sdd\validate.py --spec SPEC-001 --gate G4` devuelve `0` sin advertencias de cobertura (CA-004). `git diff -U0 -- specs/001-main-menu/spec.md` muestra solo líneas añadidas que empiezan por «Cubre:» (y líneas vacías).
- [x] Completada.
- **Evidencia:** `specs/001-main-menu/spec.md` con cinco líneas «Cubre:» añadidas, una por criterio (CA-001 a CA-005), según el mapeo de `validation_report.md`. Diff de Git: 5 inserciones, 0 eliminaciones. `validate.py --all` devuelve `0` sin las advertencias de cobertura de SPEC-001. `validate.py --spec SPEC-001 --gate G4` devuelve `0`. Archivo en CRLF; sin salto final, como en la versión previa. Ejecutada después de T-005, cuya dependencia ya estaba completada.

### T-007

- **Dependencias:** `T-006`.
- **Requisitos cubiertos:** `RF-005`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Ejecutor:** `documenter`. Solo tiene permiso sobre `docs/**` y `AGENTS.md`.
- **Estimación:** 20 min.
- **Validación:** la fila de `sdd` en §10 describe orquestación de solo lectura con bookkeeping Git. `Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern "solo lectura"` no devuelve ninguna coincidencia sin matiz de bookkeeping (CA-005). `git diff --check` devuelve `0`.
- [x] Completada.
- **Evidencia:** `docs/sdd/PROTOCOLO_OPERATIVO.md`, §10, línea 162, ejecutada por `documenter`. Texto final de la fila de `sdd`:
  `| `sdd` | Orquestador, estado y diagnóstico | Lectura de artefactos y código; puede lanzar subagentes y ejecutar bookkeeping Git (`git add`, `git commit`) de artefactos de control |`
  El límite «de artefactos de control» se añadió para cumplir RF-005: el bookkeeping Git queda acotado a artefactos de control y no se describe como lectura absoluta. El resto de la tabla no cambia.

### T-008

- **Dependencias:** `T-007`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RF-005`.
- **Archivos:** `CHANGELOG.md`, sección `## [Unreleased]`.
- **Ejecutor:** `coder`. Autorización del propietario: `coder` puede editar `CHANGELOG.md` durante el flujo de release, como en los releases v0.3.0, v0.3.1 y v0.4.0. Su configuración deniega `specs/**` y `docs/**`, pero no `CHANGELOG.md`, así que la edición está dentro de sus permisos.
- **Estimación:** 15 min.
- **Validación:** `Select-String -Path CHANGELOG.md -Pattern "SPEC-005"` muestra una entrada bajo `## [Unreleased]` que resume RF-001 a RF-005.
- **Evidencia (2026-11-13):**
  - Cambio en `CHANGELOG.md`: bajo `## [Unreleased]` se añaden `### Added` (2 entradas: G3 y G4) y `### Changed` (3 entradas: rama en specs publicadas, cobertura de SPEC-001 y bookkeeping de `sdd`), todas con `(SPEC-005)`. Ninguna línea de `## [v0.4.0]` ni anteriores ha cambiado.
  - `git diff -- CHANGELOG.md`: 11 inserciones, 0 eliminaciones.
  - Finales de línea: 150 LF y 150 CRLF; el archivo termina en CRLF (`0D 0A`).
  - `python tools\sdd\validate.py --all` → código `0`.
  - `git diff --check` → código `0`.
- [x] Completada.

### T-009

- **Dependencias:** `T-008`.
- **Requisitos cubiertos:** `CB-003`, `RNF-001`, `RNF-002`, `RNF-003`.
- **Archivos:** ninguno. Solo ejecución y lectura.
- **Estimación:** 30 min.
- **Validación:** regresión final (CA-006):
  - `python -m unittest discover -s tools\sdd\tests` devuelve `OK`.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4`, `--spec SPEC-002 --gate G4`, `--spec SPEC-001 --gate G3` y `--spec SPEC-002 --gate G3`, cada uno con código `0`.
  - `python tools\sdd\validate.py --all` devuelve `0`.
  - `git diff --check` devuelve `0`.
- **Evidencia (regresión final, 2026-11-13):**
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 47 tests`, `OK`, código `0`.
  - `python tools\sdd\validate.py --all` → código `0`. Sin advertencias de cobertura RF/CB. Única advertencia: `specs\005-compuertas-completas\validation_report.md no existe`, que corresponde al reporte del `reviewer` posterior a esta tarea.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G4` → código `0`, `OK: sin hallazgos.`.
  - `python tools\sdd\validate.py --spec SPEC-002 --gate G4 --git` → código `0`, `OK: sin hallazgos.`.
  - `python tools\sdd\validate.py --spec SPEC-005 --gate G3` → código `1`, ejecutado antes de marcar T-009. Único error: `tarea T-009 no completada (casilla [x] ausente en «Completada») con G3`. Las tareas T-001 a T-008 están completas.
  - `python tools\sdd\validate.py --spec SPEC-001 --gate G3` → código `0`, `OK: sin hallazgos.`.
  - `python tools\sdd\validate.py --spec SPEC-002 --gate G3` → código `0`, `OK: sin hallazgos.`.
  - Históricos: `python tools\sdd\validate.py --spec SPEC-003 --gate G4` → código `0`, `OK: sin hallazgos.`. `python tools\sdd\validate.py --spec SPEC-004 --gate G4` → código `0`, `OK: sin hallazgos.`.
  - `git diff --check` → código `0`, sin hallazgos.
- [x] Completada.
