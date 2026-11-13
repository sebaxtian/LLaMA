# Reporte de validación - SPEC-003

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/validacion-g4`.
- Commit auditado: `8a72b28` («feat(sdd): validacion estricta de la compuerta G4»). Árbol de trabajo limpio antes de la auditoría (`git status --short` sin salida).
- Spec auditada: `spec.md` v0.4.0 (frontmatter `status: implemented`), `clarify.md` cerrado (AMB-001 a AMB-004), `plan.md` (DEC-001 a DEC-005), `tasks.md` (T-001 a T-005, 5 de 5 completadas).
- Herramientas: Python 3.15.2, Git, `unittest` de la biblioteca estándar, validador `tools/sdd/validate.py`.
- Fecha de la auditoría: 2026-11-13. Auditor: subagente `reviewer`, independiente de `planner`, `coder` y `sdd`.
- Alcance de lectura: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/sdd/plantillas/validation_report.md`, `spec.md`, `clarify.md`, `plan.md`, `tasks.md`, `git show 8a72b28` completo (`tools/sdd/validate.py`, `tools/sdd/tests/test_validate.py`, 11 carpetas de fixtures, `specs/INDEX.md`).
- Estado de la compuerta G4: pendiente de aprobación del propietario. Este reporte no aprueba G4.

## Verificación automatizada

### Suite de pruebas

Comando: `python -m unittest discover -s tools\sdd\tests`

```text
Ran 34 tests
OK
código de salida: 0
```

Desglose de las 34 pruebas: `TestFrontmatter` 3, `TestLexicon` 5, `TestCycle` 2, `TestValidateSpec` 3 (línea base de 13); `TestDictamenG4` 4, `TestMatrizG4` 2, `TestReporteAusente` 4, `TestDependencias` 1 (11 nuevas de T-001); `TestCoberturaRF004` 3, `TestCodigosSalida` 5, `TestCoberturaReal` 2 (10 nuevas de T-003).

### Regresión y salida de SPEC-003 (códigos reales de Python)

| Comando | Salida resumida | Código |
|---|---|---|
| `python tools\sdd\validate.py --spec SPEC-001 --gate G4` | 9 advertencias de cobertura RF/CB (esperadas por AMB-003), sin errores | 0 |
| `python tools\sdd\validate.py --spec SPEC-002 --gate G4` | `OK: sin hallazgos.` | 0 |
| `python tools\sdd\validate.py --all` | 9 advertencias de SPEC-001 y 1 de reporte ausente en SPEC-003 (antes de este reporte), sin errores | 0 |
| `python tools\sdd\validate.py --spec SPEC-003 --gate G4` (ejecutada antes de escribir este reporte) | `[ERROR] specs\003-validacion-g4\validation_report.md: validation_report.md ausente (obligatorio con G4/G5/G6 o en estado validated/released)` | 1 |

Nota sobre SPEC-002: se usó sin `--git`, porque su rama ya fue integrada y eliminada.

El código `1` de SPEC-003 antes de este reporte es el comportamiento exigido por RF-001 (reporte ausente con G4). Se repite la ejecución tras escribir el reporte (ver «Ejecución final» al final).

### Verificación independiente con casos temporales

Los casos se crearon en `C:\Users\sebax\AppData\Local\Temp\opencode\` y se eliminaron al terminar. No quedó ningún archivo en el repositorio (`git status --short` limpio tras la auditoría). Se llamó a `validate_report(..., gate="G4")` con la raíz redirigida a la carpeta temporal.

| Caso | Reporte de entrada | Resultado observado |
|---|---|---|
| A | Casilla `[x] NO CONVERGIDO` marcada y `CONVERGIDO` sin marcar | ERROR: dictamen NO CONVERGIDO marcado |
| B | Prosa con «NO CONVERGIDO» más `[x] CONVERGIDO` | Sin hallazgos |
| C | Fila de matriz con estado de fallo (celda exacta, caso temporal) | ERROR: fila no superada en la matriz |
| F | `CONVERGIDO` marcado fuera de viñeta | ERROR: CONVERGIDO no marcado (fallo cerrado, DEC-001) |
| G | `[X] CONVERGIDO` en mayúscula | Sin hallazgos |
| H | Sin línea de dictamen | ERROR: CONVERGIDO no marcado |
| J1 | Spec `draft` sin reporte, compuerta G4 | ERROR por reporte ausente |
| J2 | Spec `draft` sin reporte, sin compuerta | Solo ADVERTENCIA |
| K | Matriz con estados `PENDIENTE` y `PARCIAL` y `[x] CONVERGIDO` | Sin hallazgos (ver observación O-03) |
| L | Matriz de SPEC-003 real (`coverage_gaps`) | Lista vacía: todos los RF y CB tienen «Cubre:» |

Caso G1: con `--gate G1` no se llama a `validate_report` (`if gate is None or int(gate[1]) >= 4`). Verificado por lectura del código. Mi fixture temporal de G1 falló por frontmatter propio, no por el validador, así que no se usa como evidencia.

## Matriz de trazabilidad

### Requisitos: RF, RNF, CB

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001 | `TestReporteAusente.test_tasked_con_g4_sin_reporte_es_error`; caso J1 temporal; `--spec SPEC-003 --gate G4` | Error de reporte ausente con G4 (salida arriba) | PASADO |
| RF-002 | CA-002 | `TestDictamenG4.test_no_convergido_marcado_es_error`, `test_convergido_sin_marcar_es_error`; casos A, F, H | Errores de dictamen en los fixtures y en los casos temporales | PASADO |
| RF-003 | CA-003 | `TestMatrizG4.test_fila_fallado_es_error`, `test_fila_no_pasado_es_error`; caso C | Error por fila no superada en los fixtures y en el caso temporal (ver O-02) | PASADO |
| RF-004 | CA-004 | `TestCoberturaRF004` (3 pruebas); `--spec SPEC-001 --gate G4` | `faltante` nombra RF-002 como advertencia; SPEC-001 da 9 advertencias y código 0 | PASADO |
| RF-005 | CA-005 | `TestReporteAusente.test_tasked_sin_compuerta_solo_advierte`, `test_draft_sin_compuerta_solo_advierte`; caso J2 | Solo advertencia sin compuerta y sin error en draft | PASADO |
| RNF-001 | CA-005 | `TestCodigosSalida` (5 pruebas); regresión CLI | Códigos 0, 1 y 2 verificados; las advertencias no cambian el código | PASADO |
| RNF-002 | CA-005 | `TestDependencias.test_solo_biblioteca_estandar` | Imports de `validate.py` en la biblioteca estándar | PASADO |
| RNF-003 | CA-005 | `python -m unittest discover -s tools\sdd\tests` | `Ran 34 tests`, `OK`, código 0 | PASADO |
| CB-001 | CA-002 | `TestDictamenG4.test_no_converge_en_prosa_no_cuenta`; caso B | Prosa con «NO CONVERGIDO» y casilla `[x] CONVERGIDO` sin errores | PASADO |
| CB-002 | CA-005 | `TestReporteAusente.test_draft_sin_compuerta_solo_advierte`; caso J2 | Draft sin reporte: solo advertencia | PASADO |
| CB-003 | CA-005 | `TestCoberturaReal` (2 pruebas); regresión CLI de SPEC-001 y SPEC-002 con G4 | SPEC-002 sin hallazgos; SPEC-001 sin errores y código 0 | PASADO |
| CB-004 | CA-001 | `TestReporteAusente.test_validated_sin_compuerta_es_error`; fixture `sin-reporte-validated` | Spec `validated` sin reporte y sin compuerta: error | PASADO |

Resumen de requisitos: 12 requisitos (RF-001 a RF-005, RNF-001 a RNF-003, CB-001 a CB-004). **PASADO: 12 de 12 (100 %).**

### Criterios de aceptación: CA-001 a CA-005

| CA | Cubre | Prueba / evidencia | Estado |
|---|---|---|---|
| CA-001 | RF-001, CB-004 | Escenario `draft` con G4 (caso J1) y escenario `validated` sin compuerta (fixture `sin-reporte-validated`) | PASADO |
| CA-002 | RF-002, CB-001 | Fixtures `no-convergido-marcado`, `convergido-sin-marcar`, `prosa-no-converge`; casos A, B | PASADO |
| CA-003 | RF-003 | Fixtures `fila-fallado` y `fila-no-pasado`; caso C | PASADO |
| CA-004 | RF-004 | `cobertura/faltante` (advertencia que nombra RF-002) y `cobertura/completa` (sin advertencias); SPEC-001 con G4 | PASADO |
| CA-005 | RF-005, CB-002, CB-003, RNF-001, RNF-002, RNF-003 | Pruebas de códigos de salida, guarda de dependencias, suite con `unittest`, regresión sobre SPEC-001 y SPEC-002 | PASADO |

Resumen de CA: **5 de 5 PASADO.**

### Trazabilidad de cobertura

- `RF/CB → CA`: completa. `coverage_gaps` sobre el `spec.md` real de SPEC-003 devuelve lista vacía; todos los RF-001 a RF-005 y CB-001 a CB-004 aparecen en alguna línea «Cubre:».
- `CA → prueba`: completa. Cada CA tiene al menos una prueba automatizada o un caso verificado.
- `RF/CB → T`: completa según `tasks.md` (T-001 a T-005 con «Requisitos cubiertos»).
- `evidencia → commit`: los artefactos de la spec y el código están en `8a72b28`. La fase Red de TDD queda documentada en `tasks.md`, no en el historial de Git (ver O-04).

## Brechas

Ninguna. Ningún requisito de RF-001 a RF-005, RNF-001 a RNF-003 ni CB-001 a CB-004 tiene evidencia no conforme.

## Observaciones

Observaciones sin efecto en el dictamen. Se registran para decisión del propietario o trabajo posterior.

- **O-01 - Recuento de fixtures en `tasks.md`.** T-001 dice «Fixtures nuevos: 10 carpetas en `tools/sdd/tests/fixtures/g4/`». En el commit hay 9 carpetas en `g4/` y 2 en `cobertura/`, es decir, 11 carpetas (17 archivos). No afecta a las pruebas, pero el registro es inexacto.
- **O-02 - Celdas compuestas no detectadas en la matriz (RF-003).** `failing_rows` compara cada celda con el texto exacto (DEC-002). Una celda que empieza por el estado, como `NO PASADO (2 pruebas)`, no produce error (caso D). Las pruebas y CA-003 solo cubren la celda exacta, así que el requisito literal se cumple. Si el propietario quiere que cualquier celda que empiece por el estado sea error, se necesita un cambio de DEC-002 en una spec nueva.
- **O-03 - La compuerta no exige PASADO en todas las celdas de estado.** `validate_report` solo busca `FALLADO` y `NO PASADO`. Una fila con `PENDIENTE` o `PARCIAL` no produce error si el dictamen está marcado (caso K). El protocolo (§2, G4) pide que la matriz «converge al 100 %». Esta exigencia no está en RF-003, que solo nombra FALLADO y NO PASADO. Este reporte cumple el 100 % por inspección manual de sus propias filas. Recomendación: una spec nueva o una enmienda de RF-003 si el propietario quiere que el validador lo imponga.
- **O-04 - Red de TDD no verificable en Git.** `8a72b28` agrupa pruebas, fixtures e implementación en un único commit. La secuencia Red → Green consta solo en `tasks.md` (salidas de T-001 y T-003 registradas). Es un registro, no un defecto del código.
- **O-05 - CHANGELOG sin entrada.** `CHANGELOG.md` no tiene ninguna entrada bajo `## [Unreleased]`, que está vacío. La constitución (§5) y AGENTS.md exigen registrar los cambios relevantes allí. No es un requisito de SPEC-003, pero debe corregirse antes de la integración G5. Recomendación: añadir la entrada en `[Unreleased]` en el commit de cierre.
- **O-06 - Ruta relativa en `validate_report`.** `validate_report` calcula la ruta con `relative_to(ROOT)`, así que falla con directorios de spec fuera del repositorio. Viene de la versión anterior; no afecta al uso normal, pero limita las pruebas con directorios temporales.
- **O-07 - Plan con estado obsoleto.** La sección «Estado» de `plan.md` dice `planned`, mientras `spec.md` dice `implemented`. Es un registro histórico y no altera la validación.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia PASADO).
- [ ] NO CONVERGIDO.

Resumen: **12 de 12 requisitos (RF-001 a RF-005, RNF-001 a RNF-003, CB-001 a CB-004) con evidencia PASADO (100 %); 5 de 5 CA PASADO.** Suite: 34 pruebas OK, código 0. Regresión: SPEC-001 G4 código 0, SPEC-002 G4 código 0, `--all` código 0. SPEC-003 G4 antes de este reporte: código 1 por reporte ausente, comportamiento exigido por RF-001.

Las observaciones O-02, O-03 y O-05 son decisiones o correcciones para el propietario o para el siguiente paso. No son brechas de los requisitos de SPEC-003.

## Ejecución final

Comando: `python tools\sdd\validate.py --spec SPEC-003 --gate G4`, ejecutado después de escribir este reporte.

```text
OK: sin hallazgos.
código de salida: 0
```

Suite tras escribir el reporte: `python -m unittest discover -s tools\sdd\tests` → `Ran 34 tests`, `OK`, código 0.

## Aprobación

- [ ] G4: `- Approved by: Agent Sebaxtian` (pendiente; solo el propietario puede aprobar).

> El dictamen CONVERGIDO indica que la matriz cumple el 100 % de los requisitos con evidencia PASADO. No aprueba G4: la aprobación es exclusiva del propietario.
