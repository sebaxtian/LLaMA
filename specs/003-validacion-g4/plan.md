# Plan técnico - SPEC-003

## Estado

- Spec: `planned` (`spec.md` v0.2.0 con G1 aprobada; clarify cerrado).
- Alcance: endurecer las comprobaciones del validador determinista para la compuerta G4 y la cobertura RF/CB → CA. Sin cambios de formato de artefactos ni de códigos de salida.

## Referencias

- `specs/003-validacion-g4/spec.md` v0.2.0: RF-001 a RF-005, RNF-001 a RNF-003, CB-001 a CB-004, CA-001 a CA-005.
- `specs/003-validacion-g4/clarify.md`: AMB-001 a AMB-004, cerrado.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §4 (contrato de `validation_report.md`), §9 (validador determinista y códigos de salida).
- `specs/002-orquestacion-subagentes-sdd/validation_report.md`: observación O-01 (el validador acepta «NO CONVERGIDO»).
- `specs/002-orquestacion-subagentes-sdd/plan.md`: brecha B-05 (cobertura RF/CB → CA sin verificar).
- `tools/sdd/validate.py`: `validate_report`, `validate_spec`, `main`.
- `tools/sdd/tests/test_validate.py`: pruebas existentes (se conservan).

## Arquitectura de módulos

Estado actual del módulo `tools/sdd/validate.py`:

- `validate_report` busca la subcadena `CONVERGIDO`. Su control de filas usa un patrón que no detecta filas reales de la tabla. No recibe la compuerta solicitada, así que su ausencia siempre produce una advertencia.
- `validate_spec` no comprueba la cobertura de requisitos por criterios.

Cambios previstos. Todo ocurre dentro del mismo módulo, sin archivos nuevos de código:

1. `validate_report(spec_id, spec_dir, rep, gate)` recibe la compuerta. Si el reporte no existe, decide la severidad con `report_required` (DEC-003). Si existe, evalúa el dictamen con `parse_dictamen` (DEC-001) y las filas con `failing_rows` (DEC-002).
2. `validate_spec` llama a `coverage_gaps` sobre el cuerpo de la spec y emite una advertencia por requisito no cubierto (DEC-004).
3. `main` pasa `gate` a `validate_report` en la rama `--spec` y en la rama `--all`.

Sin cambios en `Reporter`, en los códigos de salida (`0`, `1`, `2`), en los formatos de los artefactos ni en los demás validadores.

Flujo resultante:

```text
main --gate G?
 └─ validate_report(gate)
     ├─ reporte ausente → report_required → error | advertencia
     └─ reporte presente
         ├─ parse_dictamen → error si NO CONVERGIDO marcado o CONVERGIDO sin marcar
         └─ failing_rows   → error por cada fila FALLADO o NO PASADO
validate_spec
 └─ coverage_gaps → advertencia por cada RF/CB sin «Cubre:»
```

## Esquemas, tipos e interfaces

Constantes nuevas en `validate.py`:

```python
DICTAMEN_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(NO CONVERGIDO|CONVERGIDO)\b", re.MULTILINE)
FAILING_CELLS = {"FALLADO", "NO PASADO"}
GATES_REQUIRING_REPORT = {"G4", "G5", "G6"}
STATES_REQUIRING_REPORT = {"validated", "released"}
```

Funciones puras nuevas (sin efectos secundarios, comprobables con cadenas en memoria):

```python
def parse_dictamen(text: str) -> dict[str, bool]
    # {"CONVERGIDO": bool, "NO CONVERGIDO": bool}. Una casilla ausente cuenta como False.

def failing_rows(text: str) -> list[str]
    # Líneas de tabla (que empiezan por "|") con una celda cuyo texto exacto está en FAILING_CELLS.

def report_required(gate: str | None, status: str) -> bool
    # True si gate está en GATES_REQUIRING_REPORT o status está en STATES_REQUIRING_REPORT.

def coverage_gaps(spec_body: str) -> list[str]
    # IDs RF-NNN o CB-NNN declarados en «Requisitos funcionales» o «Casos borde» que no aparecen en ninguna línea «Cubre:» de la sección de criterios.
```

Firma modificada de una función existente:

```python
def validate_report(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None) -> None
```

Tipos existentes sin cambios: `Reporter`, `Finding`.

## Decisiones técnicas

### DEC-001 - Dictamen por casilla marcada anclada a inicio de línea

- **Contexto:** AMB-004. La búsqueda de la subcadena `CONVERGIDO` acepta «NO CONVERGIDO».
- **Decisión:** `DICTAMEN_RE` solo reconoce líneas de viñeta con casilla `[x]`, `[ ]` o `[X]` seguida de `CONVERGIDO` o `NO CONVERGIDO`. El error se emite si `NO CONVERGIDO` está marcada, o si `CONVERGIDO` no está marcada, incluida la ausencia de la línea. La prosa no se evalúa.
- **Alternativas descartadas:** buscar `[x] CONVERGIDO` en cualquier posición del texto. Se descarta porque una cita dentro de una frase la aceptaría.
- **Consecuencias:** un dictamen fuera de viñeta no se reconoce y produce error. El fallo es cerrado.

### DEC-002 - Filas no superadas solo en líneas de tabla

- **Contexto:** RF-003. El patrón actual no reconoce filas reales.
- **Decisión:** se analizan solo las líneas que empiezan por `|` tras quitar espacios. Cada celda se compara con el texto exacto (sin espacios sobrantes) contra `FAILING_CELLS`. Cualquier coincidencia es un error.
- **Alternativas descartadas:** buscar `FALLADO` o `NO PASADO` en todo el texto. Se descarta porque una mención en prosa, como «ninguna fila queda en NO PASADO», produciría un falso error.
- **Consecuencias:** una tabla sin barras iniciales no se analiza. Es un formato no válido del contrato de la plantilla.

### DEC-003 - Cuándo la ausencia de reporte es error

- **Contexto:** RF-001, RF-005, CB-002 y CB-004.
- **Decisión:** `report_required(gate, status)` devuelve `True` si la compuerta solicitada es G4, G5 o G6, o si el estado es `validated` o `released`. Si es `True`, la ausencia del reporte es un error. En otro caso, es una advertencia.
- **Alternativas descartadas:** error siempre que falte el reporte. Se descarta porque rompería las specs en borrador (RF-005).
- **Consecuencias:** con `--all` y sin compuerta, una spec `validated` o `released` sin reporte produce error. Con `--spec` y compuertas G1 a G3, `validate_report` no se llama (sin cambio).

### DEC-004 - Cobertura RF/CB → CA mediante líneas «Cubre:»

- **Contexto:** RF-004 y AMB-003.
- **Decisión:** `coverage_gaps` toma los requisitos de los encabezados `### RF-NNN` de «Requisitos funcionales» y `### CB-NNN` de «Casos borde». Toma los identificadores de las líneas que empiezan por «Cubre:» dentro de la sección «Criterios de aceptación». Cada requisito sin cobertura genera una advertencia que lo nombra. Los RNF quedan fuera de esta comprobación.
- **Alternativas descartadas:** error en lugar de advertencia. Se descarta por AMB-003 y porque SPEC-001 no declara «Cubre:».
- **Consecuencias:** SPEC-001 recibirá advertencias de cobertura. Es el resultado esperado y está aceptado (AMB-003, CB-003).

### DEC-005 - Mecanismo de pruebas: `unittest`

- **Contexto:** AMB-002 y RNF-003.
- **Decisión:** `unittest` de la biblioteca estándar. Comando único desde la raíz: `python -m unittest discover -s tools\sdd\tests`.
- **Alternativas descartadas:** `pytest`. Se descarta porque es una dependencia externa (RNF-002, constitución §4).
- **Consecuencias:** las pruebas dependen solo de la biblioteca estándar, y el comando es el mismo en cualquier equipo Windows con Python.

## Estrategia de testing

Principio: Red antes de Green. Cada tarea declara su salida esperada en `tasks.md`.

Niveles:

1. **Unitarias sobre funciones puras.** `parse_dictamen`, `failing_rows`, `report_required` y `coverage_gaps` se prueban con cadenas en memoria. Cubren DEC-001 a DEC-004.
2. **Integración sobre fixtures de reportes.** `validate_report` se ejecuta sobre `tools/sdd/tests/fixtures/g4/<caso>/`, que contiene `spec.md` (para leer el estado) y, cuando aplica, `validation_report.md`.
3. **Códigos de salida.** `main` se ejecuta con `SPECS_DIR` redirigido a un fixture mediante `unittest.mock.patch`. Comprueba los códigos `0`, `1` y `2` (RNF-001).
4. **Guarda de dependencias.** Las importaciones del módulo se comparan con `sys.stdlib_module_names` (RNF-002).
5. **Regresión sobre reportes reales.** `validate_report` con `gate="G4"` sobre `specs/001-main-menu` y `specs/002-orquestacion-subagentes-sdd` debe devolver cero errores (CB-003). Se repite con `--all`.

Fixtures previstos (no existen aún):

| Carpeta | Contenido | Resultado esperado con G4 o estado `validated` |
|---|---|---|
| `fixtures/g4/dictamen-ok` | `[x] CONVERGIDO`, matriz PASADO | sin errores |
| `fixtures/g4/prosa-no-converge` | «NO CONVERGIDO» en prosa, `[x] CONVERGIDO` | sin errores (CB-001) |
| `fixtures/g4/no-convergido-marcado` | `[x] NO CONVERGIDO` | error (RF-002) |
| `fixtures/g4/convergido-sin-marcar` | `[ ] CONVERGIDO` | error (RF-002) |
| `fixtures/g4/fila-fallado` | una fila con `FALLADO` | error (RF-003) |
| `fixtures/g4/fila-no-pasado` | una fila con `NO PASADO` | error (RF-003) |
| `fixtures/g4/sin-reporte-tasked` | `spec.md` en `tasked`, sin reporte | error con G4; advertencia sin compuerta (RF-001, RF-005) |
| `fixtures/g4/sin-reporte-draft` | `spec.md` en `draft`, sin reporte | advertencia sin compuerta, sin error (CB-002) |
| `fixtures/g4/sin-reporte-validated` | `spec.md` en `validated`, sin reporte | error sin compuerta (CB-004) |
| `fixtures/cobertura/completa` | todos los RF y CB aparecen en «Cubre:» | sin advertencias de cobertura |
| `fixtures/cobertura/faltante` | un RF no aparece en «Cubre:» | advertencia que nombra ese RF (RF-004) |

Comandos de verificación:

- `python -m unittest discover -s tools\sdd\tests` (código `0` al final, código `1` en las tareas en rojo).
- `python tools\sdd\validate.py --all` (código `0`).
- `python tools\sdd\validate.py --spec SPEC-001 --gate G4` y `--spec SPEC-002 --gate G4` (código `0`).

## Matriz de cobertura

| Requisito | CA | Componente | Prueba | Tarea |
|---|---|---|---|---|
| RF-001 | CA-001 | `validate_report`, `report_required` | `sin-reporte-tasked` con G4 | T-001, T-002 |
| RF-002 | CA-002 | `parse_dictamen` | `no-convergido-marcado`, `convergido-sin-marcar` | T-001, T-002 |
| RF-003 | CA-003 | `failing_rows` | `fila-fallado`, `fila-no-pasado` | T-001, T-002 |
| RF-004 | CA-004 | `coverage_gaps`, `validate_spec` | `cobertura/faltante`, `cobertura/completa` | T-003, T-004 |
| RF-005 | CA-005 | `report_required` | `sin-reporte-draft`, `sin-reporte-tasked` sin compuerta | T-001, T-002 |
| RNF-001 | CA-005 | `main` | códigos `0`, `1`, `2` con `SPECS_DIR` redirigido | T-003, T-004, T-005 |
| RNF-002 | CA-005 | importaciones del módulo | guarda con `sys.stdlib_module_names` | T-001, T-005 |
| RNF-003 | CA-005 | comando `unittest discover` | ejecución completa | T-005 |
| CB-001 | CA-002 | `parse_dictamen` | `prosa-no-converge` | T-001, T-002 |
| CB-002 | CA-005 | `report_required` | `sin-reporte-draft` | T-001, T-002 |
| CB-003 | CA-005 | `validate_report` (regresión real) | SPEC-001 y SPEC-002 con G4 | T-005 |
| CB-004 | CA-001 | `report_required` | `sin-reporte-validated` sin compuerta | T-001, T-002 |
