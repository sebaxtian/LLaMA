# Reporte de validación - SPEC-005

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/compuertas-completas`.
- Commit auditado: `03203ca` («feat(sdd): compuertas completas y cierre de deuda residual»). Árbol de trabajo limpio (`git status --short` sin salida).
- Spec auditada: `spec.md` v0.4.0, `status: implemented`, con `clarify.md` cerrado (AMB-001 a AMB-003), `plan.md` (DEC-001 a DEC-006) y `tasks.md` (T-001 a T-009, 9 de 9 completadas).
- Herramientas: Python 3.15.2, validador `tools/sdd/validate.py`, suite `tools/sdd/tests` (`unittest`).
- Alcance de lectura: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` (§10), `specs/005-compuertas-completas/{spec,clarify,plan,tasks}.md`, `specs/001-main-menu/{spec,validation_report}.md`, `git show 03203ca` completo y fixtures de `tools/sdd/tests/fixtures/`.
- Fecha de la auditoría: 2026-11-13. Auditor: subagente `reviewer`, independiente de `planner`, `coder` y `sdd`.

### Resultados de ejecución

| Comando | Resultado | Código |
|---|---|---|
| `python -m unittest discover -s tools\sdd\tests` | `Ran 47 tests`, `OK` | 0 |
| `python tools\sdd\validate.py --all` | Solo `[WARN]` por `specs\005-compuertas-completas\validation_report.md` no existe (antes de este reporte) | 0 |
| `python tools\sdd\validate.py --spec SPEC-001 --gate G4` | `OK: sin hallazgos.` | 0 |
| `python tools\sdd\validate.py --spec SPEC-002 --gate G4 --git` | `OK: sin hallazgos.` | 0 |
| `python tools\sdd\validate.py --spec SPEC-003 --gate G4` | `OK: sin hallazgos.` | 0 |
| `python tools\sdd\validate.py --spec SPEC-004 --gate G4` | `OK: sin hallazgos.` | 0 |
| `python tools\sdd\validate.py --spec SPEC-005 --gate G3` | `OK: sin hallazgos.` (las 9 tareas están marcadas) | 0 |
| `python tools\sdd\validate.py` (sin argumentos) | error de uso | 2 |
| `git --no-pager show --check 03203ca` | sin hallazgos de espacios | 0 |

### Comprobaciones manuales de comportamiento nuevo

Se ejecutaron con funciones del validador importadas desde `tools/sdd/validate.py` y con copias temporales de fixtures en un directorio temporal fuera del repositorio. No se modificó nada del repositorio.

- **G4, celdas de estado (RF-002):** `PENDIENTE`, `PARCIAL`, `PASADO / FALLADO`, `NO PASADO` y celda vacía producen una entrada de error por fila cada una. Tabla de trazabilidad sin columna de estado produce error. Verificado con `not_passed_rows`.
- **G4, observación (CB-001):** `PASADO (con observación O-16)`, `  pasado   (obs)  ` y `PASADO` no producen error. `PASADO (x) extra` sí produce error, consistente con la regla de PASADO seguido solo de paréntesis.
- **G4, tabla ajena (CB-001 / DEC-002):** tabla `| Brecha | Estado |` con `CERRADA` no produce error. Una columna `Evidencia` con texto «FALLADO» en una fila con estado `PASADO` tampoco produce error.
- **G3 con tarea pendiente (RF-001):** con `g3/tarea-pendiente` y gate G3, `main` devuelve 1 y el error nombra la tarea: `tarea T-002 no completada (casilla [x] ausente en «Completada») con G3`. La línea de progreso `- [x] 2 de 2` fuera de bloque no cuenta.
- **Rama en released/superseded (RF-003, CB-002), con `--git` real:** una copia de `released-rama-eliminada` (rama `feat/rama-eliminada`) en `released` devuelve 0 sin error de rama; la misma copia en `superseded` devuelve 0 sin error de rama. Control: copia de `validated-rama-distinta` (rama `feat/rama-declarada`) en `validated` devuelve 1 con `rama actual 'feat/compuertas-completas' no coincide con la declarada 'feat/rama-declarada'`. El comportamiento es el esperado.

## Matriz de trazabilidad

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001 | `TestG3Tareas` (3 pruebas); `--spec SPEC-005 --gate G3` devuelve 0; copia temporal de `g3/tarea-pendiente` con G3 devuelve 1 y nombra `T-002` | `Ran 47 tests` OK; salidas indicadas arriba | PASADO |
| RF-002 | CA-002 | `TestMatrizEstados` (8 pruebas); comprobación manual de PENDIENTE, PARCIAL, `PASADO / FALLADO`, `NO PASADO`, celda vacía y tabla sin columna de estado | Cada caso produce error; la suite pasa | PASADO |
| RF-003 | CA-003 | `TestRamaEstado` con `git_checks` simulado; comprobación manual con `--git` real sobre `released`, `superseded` y control `validated` | `released` y `superseded` con rama inexistente devuelven 0 sin error de rama; `validated` con rama distinta devuelve 1 | PASADO |
| RF-004 | CA-004 | `git --no-pager show 03203ca -- specs/001-main-menu/spec.md`: 5 inserciones, 0 eliminaciones, solo líneas `Cubre:`; mapeo comparado con `specs/001-main-menu/validation_report.md`; `--spec SPEC-001 --gate G4` devuelve 0 sin advertencias | Mapeo idéntico: CA-001 {RF-001, RF-003, RNF-001}; CA-002 {RF-002, RNF-002, CB-002}; CA-003 {RF-004}; CA-004 {RF-005, CB-001}; CA-005 {RF-006, CB-003} | PASADO |
| RF-005 | CA-005 | Lectura de `docs/sdd/PROTOCOLO_OPERATIVO.md` §10, línea 162; búsqueda de «solo lectura» en el protocolo (sin coincidencias en §10) | La fila de `sdd` describe «Lectura de artefactos y código» con bookkeeping Git (`git add`, `git commit`) de artefactos de control. Ver observación O-1 | PASADO |
| RNF-001 | CA-006 | `TestCodigosSalida` (códigos 0, 1 y 2); `validate.py` sin argumentos devuelve 2; validaciones de esta auditoría devuelven 0 o 1 según corresponde | Códigos 0, 1 y 2 verificados | PASADO |
| RNF-002 | CA-006 | `TestDependencias.test_solo_biblioteca_estandar`; revisión de importaciones de `validate.py` | Suite OK; solo biblioteca estándar | PASADO |
| RNF-003 | CA-006 | `python -m unittest discover -s tools\sdd\tests` (sin dependencias externas) | `Ran 47 tests`, `OK`, código 0 | PASADO |
| CB-001 | CA-002 | `TestMatrizEstados.test_observacion_no_es_error` y `test_pasado_fallado_es_error`; comprobación manual de `PASADO (con observación O-16)` | Observación: sin error. `PASADO / FALLADO`: error | PASADO |
| CB-002 | CA-003 | `TestRamaEstado.test_released_rama_eliminada_sin_error_de_rama`; comprobación manual con `--git` real | Sin error de rama en `released` con rama inexistente | PASADO |
| CB-003 | CA-006 | `--spec SPEC-001 --gate G4`, `--spec SPEC-002 --gate G4 --git`, `--spec SPEC-003 --gate G4`, `--spec SPEC-004 --gate G4`, todos con código 0 | Históricos válidos con la regla nueva | PASADO |

Cobertura de requisitos: RF-001 a RF-005, RNF-001 a RNF-003 y CB-001 a CB-003 (11 de 11) están cubiertos por los CA-001 a CA-006 de `spec.md`. Los CA-001 a CA-006 tienen tarea de implementación en `tasks.md` (T-001 a T-009). Cada requisito tiene evidencia `PASADO`.

## Brechas

- Ninguna brecha bloqueante. Ningún requisito tiene evidencia distinta de `PASADO`.

### Observaciones no bloqueantes

- **O-1 (RF-005):** §10 describe a `sdd` como «Lectura de artefactos y código; puede lanzar subagentes y ejecutar bookkeeping Git (`git add`, `git commit`) de artefactos de control». RF-005 pide la expresión «orquestador de solo lectura sobre artefactos y código». La fila cumple su sentido (lectura más bookkeeping acotado y sin lectura absoluta) y CA-005 se satisface, por lo que se marca `PASADO`. Si el propietario exige la expresión literal, el ajuste corresponde a `documenter` (`docs/**`), no a este reporte.
- **O-2 (AMB-001):** `clarify.md` deja pendiente para el propietario confirmar la forma de la regla de celda superada (PASADO con paréntesis opcional, sin prefijo). La aprobación G1 registrada en `spec.md` cubre la spec, pero el propietario debe confirmar este punto de forma explícita en su revisión G4.
- **O-3 (alcance del validador):** la compuerta G3 solo se aplica con `--gate G3` explícito, incluido `--all`, y no por estado. Es la decisión de `tasks.md` (T-002) y no contradice RF-001 ni CA-001. Se registra para que el propietario la conozca.
- **O-4 (fuera de alcance):** la comprobación `--git` no se aplica en `--all`. Es comportamiento anterior a SPEC-005, no cambiado por el commit.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia `PASADO`: 11 de 11).
- [ ] NO CONVERGIDO

## Aprobación

- [ ] G4: pendiente de aprobación del propietario. Este reporte no aprueba la compuerta G4.
