# Plan técnico - SPEC-005

## Referencias

- `spec.md`: `SPEC-005`, versión 0.2.0 (estado `clarified`, G1 aprobada el 2026-11-13).
- `clarify.md`: `SPEC-005`, cerrado con AMB-001 a AMB-003 y parches aplicados.
- Código afectado: `tools/sdd/validate.py` y `tools/sdd/tests/test_validate.py`.
- Referencia de datos: `specs/001-main-menu/spec.md` y `specs/001-main-menu/validation_report.md` (mapeo de cobertura, DEC-005); `specs/002-orquestacion-subagentes-sdd/validation_report.md` (regresión de CB-003).

## Arquitectura de módulos

El cambio se limita a cuatro puntos del validador. Ningún otro componente cambia salvo los artefactos listados.

1. **Compuerta G3 (RF-001).** `validate_tasks` recibe la compuerta solicitada. Con G3, cuenta las tareas cuyo bloque no tiene la casilla `[x]` en la línea «Completada». Cada tarea incompleta produce un error (DEC-001).
2. **Matriz de trazabilidad (RF-002, CB-001).** `failing_rows` se sustituye por una función que localiza las tablas de trazabilidad y evalúa la columna de estado de cada fila (DEC-002 y DEC-003). `validate_report` usa la nueva función.
3. **Rama declarada (RF-003, CB-002).** `main` pasa la rama declarada a `git_checks` solo si el estado no es `released` ni `superseded` (DEC-004). El resto de `git_checks` no cambia.
4. **Artefactos fuera del validador.** La línea «Cubre:» de SPEC-001 (RF-004, DEC-005) y la fila de `sdd` en §10 de `docs/sdd/PROTOCOLO_OPERATIVO.md` (RF-005, DEC-006). La entrada de `CHANGELOG.md` queda a cargo del propietario (ver T-008).

El validador conserva los códigos de salida `0`, `1` y `2` (RNF-001) y solo usa la biblioteca estándar (RNF-002).

## Esquemas, tipos e interfaces

- `validate_tasks(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None = None) -> None`. El parámetro nuevo se pasa desde `main` en ambas ramas (`--spec` y `--all`).
- `incomplete_tasks(text: str) -> list[str]`. Devuelve los identificadores `T-NNN` de los bloques `### T-NNN` cuyo bloque no contiene la línea `- [x] Completada`. La línea de progreso `- [ ] N de M tareas completadas` queda fuera de cualquier bloque y no cuenta.
- `STATUS_COLUMNS = {"estado", "resultado"}`. Columnas de estado. «Resultado» se admite porque los fixtures de G4 la usan.
- `TRACE_FIRST_HEADERS = {"requisito", "criterio", "ca"}`. Primera cabecera que identifica una tabla de trazabilidad.
- `PASSED_CELL_RE = re.compile(r"^PASADO(\s*\([^()]*\))?$")`. Se aplica al texto de la celda normalizado (DEC-003).
- `not_passed_rows(text: str) -> list[str]`. Devuelve las filas de datos de las tablas de trazabilidad cuya celda de estado no cumple `PASSED_CELL_RE`. Si una tabla de trazabilidad no tiene columna de estado, devuelve una entrada que describe la ausencia.
- `NO_BRANCH_CHECK_STATES = {"released", "superseded"}`.

## Decisiones técnicas

### DEC-001

- **Decisión:** G3 cuenta tareas con la casilla marcada dentro del bloque de cada tarea (`### T-NNN`, línea «Completada»). Una tarea sin esa línea o con la casilla vacía es incompleta.
- **Alternativas descartadas:** contar todas las casillas `[x]` del archivo. Se descarta porque la línea de progreso (`[x] 4 de 4`) y cualquier otra casilla inflarían el recuento y darían falsos positivos.

### DEC-002

- **Decisión:** se evalúan solo las tablas cuya primera cabecera es `Requisito`, `Criterio` o `CA`, y solo las filas de datos (no la cabecera ni la línea `|---|`). Dentro de cada tabla se usa la columna cuya cabecera es `Estado` o `Resultado`. Si la tabla de trazabilidad no tiene esa columna, es un error.
- **Alternativas descartadas:**
  - Evaluar cualquier tabla con cabecera «Estado». Se descarta: los reportes de SPEC-002 tienen tablas «Verificación | Resultado | Estado» y «Brecha | Estado» con valores «Conforme…» y «CERRADA». Esas tablas no son trazabilidad y darían errores falsos, lo que rompería CB-003.
  - Evaluar cualquier celda de la fila (comportamiento actual). Se descarta: una celda de evidencia que contenga «FALLADO» daría un error falso, y no detecta de forma precisa la celda de estado.
- **Nota:** la decisión del propietario era «cabecera con Estado». Esta forma la precisa para excluir tablas que no son de trazabilidad. Se registra en `clarify.md` como precisión de AMB-001.

### DEC-003

- **Decisión:** una celda cuenta como superada si, tras normalizar espacios (`strip` y colapsar espacios internos) y mayúsculas, coincide con `PASADO` seguido opcionalmente de un paréntesis de observación (`PASSED_CELL_RE`). Una celda vacía no es superada. El contenido del paréntesis no se interpreta.
- **Alternativas descartadas:** prefijo «empieza por PASADO». Se descarta porque aceptaría «PASADO / FALLADO» (RF-002 y CA-002 lo exigen como error).
- **Nota:** esta es la precisión de AMB-001 que requiere confirmación del propietario (ver `clarify.md`).

### DEC-004

- **Decisión:** `main` omite la rama declarada cuando el estado de la spec es `released` o `superseded`. `git_checks` recibe `None` en esos casos y no compara ramas. Las comprobaciones de commits no cambian.
- **Alternativas descartadas:** emitir una advertencia en lugar de omitir. Se descarta porque el propietario quiere que no haya ruido en specs integradas, y una advertencia en cada spec released sería ruido permanente.

### DEC-005

- **Decisión:** la línea «Cubre:» de cada criterio de SPEC-001 se deriva de la matriz de su `validation_report.md`:
  - CA-001: `RF-001`, `RF-003`, `RNF-001`.
  - CA-002: `RF-002`, `RNF-002`, `CB-002`.
  - CA-003: `RF-004`.
  - CA-004: `RF-005`, `CB-001`.
  - CA-005: `RF-006`, `CB-003`.
  Solo se añaden esas líneas. Requisitos, criterios, frontmatter y reporte no cambian.
- **Alternativas descartadas:** convertir la advertencia de cobertura en error. Queda fuera de alcance según `spec.md`.

### DEC-006

- **Decisión:** la fila de `sdd` en §10 pasa a describirse como orquestador de solo lectura sobre artefactos y código, con bookkeeping Git (`git add`, `git commit`) de artefactos de control, ejecución del validador y lanzamiento de subagentes. El resto de la tabla no cambia.
- **Alternativas descartadas:** describirlo como lectura y escritura. Se descarta porque contradice AMB-003: `sdd` no escribe artefactos ni código.

## Estrategia de testing

- **Comando único de pruebas:** `python -m unittest discover -s tools\sdd\tests`, ejecutado desde la raíz del repositorio. No requiere `-t`.
- **TDD:** las pruebas de G3 (T-001) y de la matriz (T-003) se escriben primero y deben fallar. Después se implementa el mínimo (T-002, T-004). La rama (T-005) se prueba con una comprobación de llamada, sin ejecutar Git real.
- **Fixtures nuevos** bajo `tools/sdd/tests/fixtures/`:
  - `g3/tareas-completas/` y `g3/tarea-pendiente/`: `spec.md` y `tasks.md`. La spec cubre `RF-001` y `CB-001` en «Requisitos cubiertos».
  - `matriz/observacion/`: celda «PASADO (con observación)». Debe pasar (CA-002).
  - `matriz/compuesta/`: celda «PASADO / FALLADO». Debe fallar (CA-002).
  - `matriz/fallado/` y `matriz/no-pasado/` ya existen en `g4/` y se reutilizan.
  - `matriz/sin-columna-estado/`: tabla de trazabilidad sin columna de estado. Debe fallar.
  - `matriz/celda-vacia/`: columna de estado vacía. Debe fallar.
  - `matriz/tabla-ajena/`: tabla «Brecha | Estado» con «CERRADA» fuera de trazabilidad. No debe producir errores.
  - `rama/released-rama-eliminada/`: estado `released` con rama inexistente (CA-003).
- **Regresión (CB-003):** pruebas existentes `TestCoberturaReal` y `TestCodigosSalida`, más comandos de T-009: `--spec SPEC-001 --gate G4`, `--spec SPEC-002 --gate G4`, `--spec SPEC-001 --gate G3`, `--spec SPEC-002 --gate G3` y `--all`. Todos deben devolver `0`.
- **Dependencias (RNF-002):** `TestDependencias` se mantiene.
- **Códigos (RNF-001):** `TestCodigosSalida` más un caso G3 con tarea pendiente (código `1`).

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | `validate_tasks` con gate G3, `incomplete_tasks` | CA-001: `TestG3Tareas` con `g3/tarea-pendiente` (error) y `g3/tareas-completas` (sin error) |
| RF-002 | `not_passed_rows`, `validate_report` | CA-002: `TestMatrizEstados` con `matriz/compuesta`, `g4/fila-fallado` y `g4/fila-no-pasado` |
| RF-003 | `main`, `NO_BRANCH_CHECK_STATES` | CA-003: `TestRamaEstado` con llamada simulada a `git_checks` (sin Git real) |
| RF-004 | `specs/001-main-menu/spec.md` (líneas «Cubre:») | CA-004: `TestCoberturaReal.test_spec001...` (ya existente) y `git diff -U0` sobre `spec.md` de SPEC-001 |
| RF-005 | `docs/sdd/PROTOCOLO_OPERATIVO.md` §10 | CA-005: lectura de §10 y búsqueda de «solo lectura» (solo con matiz de bookkeeping) |
| RNF-001 | `main`, códigos de salida | CA-006: `TestCodigosSalida` y comandos de T-009 |
| RNF-002 | importaciones de `validate.py` | CA-006: `TestDependencias.test_solo_biblioteca_estandar` |
| RNF-003 | suite con `unittest` | CA-006: `python -m unittest discover -s tools\sdd\tests` |
| CB-001 | `PASSED_CELL_RE`, `not_passed_rows` | CA-002: `TestMatrizEstados.test_observacion_no_es_error` con `matriz/observacion` |
| CB-002 | `main` con estado `released` | CA-003: `TestRamaEstado.test_released_rama_eliminada` |
| CB-003 | validador completo y reportes reales | CA-006: `TestCoberturaReal`, `--all` y comandos de regresión de T-009 |
