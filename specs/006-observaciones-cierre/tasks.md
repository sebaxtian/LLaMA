# Tareas - SPEC-006

## Progreso

- [x] 5 de 5 tareas completadas.

## Notas de permisos

Permisos verificados con `opencode debug agents` desde la raíz del repositorio:

- `documenter`: edición solo de `docs/**` y `AGENTS.md`. Puede ejecutar T-001.
- `coder`: edición general, excepto `specs/**` y `docs/**`. Puede ejecutar T-002 y T-004 sobre `MEMORY.md` y `CHANGELOG.md`.
- `planner`: edición solo de `specs/**`. Puede ejecutar T-003.
- `reviewer`: edición solo de `validation_report.md`, con ejecución de comandos permitida. Puede ejecutar T-005.

Si una tarea requiere un permiso distinto del asignado, se aplica CB-001 de `spec.md`: el ejecutor se detiene, no modifica nada y reporta.

## Tareas

Orden de ejecución: T-001, T-002 y T-003 son independientes entre sí. T-004 va después de ellas y T-005 al final.

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-001`, `CB-001`, `RNF-001`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Estimación:** 20 min.
- **Validación:** `Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern "orquestador de solo lectura sobre artefactos y código" -SimpleMatch -CaseSensitive:$false` devuelve la fila de `sdd` dentro de §10. La fila limita el bookkeeping Git a artefactos de control. Ningún otro texto del protocolo cambia.
- **Evidencia (T-001, ejecutada por `documenter`; registro por `coder`, 2026-11-13):**
  - `Select-String -Path docs\sdd\PROTOCOLO_OPERATIVO.md -Pattern "Orquestador de solo lectura sobre artefactos y código" -SimpleMatch` → coincidencia en la línea 162, dentro de §10.
  - Fila de `sdd` en §10 (primera fila de la tabla de agentes): `| \`sdd\` | Orquestador de solo lectura sobre artefactos y código; estado y diagnóstico | Puede lanzar subagentes y ejecutar \`git add\` y \`git commit\` de artefactos de control |`. El bookkeeping queda limitado a artefactos de control.
  - `git diff -- docs/sdd/PROTOCOLO_OPERATIVO.md`: una línea eliminada y una añadida, ambas en la fila de `sdd`. Ningún otro texto cambia.
- [x] Completada.

### T-002

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-002`, `CB-002`, `RNF-001`.
- **Archivos:** `MEMORY.md`.
- **Estimación:** 25 min.
- **Validación:** `Select-String -Path MEMORY.md -Pattern "documenter"` encuentra la lista de agentes. La línea de `.opencode/` enumera `sdd`, `planner`, `coder`, `reviewer` y `documenter`, y `explore` figura como integrado. La viñeta de consulta contiene `opencode debug agents` y la advertencia de directorio. Ejecutar el comando desde la raíz lista `sdd`, `planner`, `coder`, `reviewer` y `documenter`. Ejecutarlo desde otro directorio no los lista.
- **Evidencia (T-002, 2026-11-13):**
  - Verificación previa: `opencode debug agents` desde la raíz (código `0`) lista `sdd`, `planner`, `coder`, `reviewer`, `documenter`, además de los integrados `Build`, `Compaction`, `Explore`, `General`, `Plan`, `Summary`, `Title`.
  - `opencode api get '/api/agent?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` (código `0`) devuelve `location.directory` del proyecto y la lista de agentes con sus permisos.
  - `opencode api get '/api/agent'` (sin parámetro, código `0`) devuelve `{"location":{"directory":"C:\\Users\\sebax"},"data":[]}`: directorio por defecto y sin agentes del proyecto. Confirma la advertencia de la viñeta.
  - `MEMORY.md`: la viñeta de `.opencode/` enumera `sdd`, `planner`, `coder`, `reviewer` y `documenter`, y declara `explore` como subagente integrado. Se añade la viñeta «Consulta de agentes» justo después.
  - `git diff -- MEMORY.md`: 1 línea eliminada y 2 añadidas, todas en el mapa operativo (la viñeta de `.opencode/` sustituida y la viñeta nueva).
  - `python tools\sdd\validate.py --all` → código `0`. `AGENTS.md` tiene 42 líneas útiles, dentro del rango 30–70. Única advertencia: `specs\006-observaciones-cierre\validation_report.md no existe`, que corresponde a la etapa de validación.
  - `MEMORY.md` mantiene CRLF (130 LF, 130 CRLF) y termina en CRLF.
  - `git diff --check` → código `0`.
- [x] Completada.

### T-003

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-003`, `RNF-001`.
- **Archivos:** `specs/005-compuertas-completas/clarify.md`.
- **Estimación:** 15 min.
- **Validación:** `Select-String -Path specs\005-compuertas-completas\clarify.md -Pattern "Nota de confirmación (SPEC-006)"` encuentra la nota al final del archivo. La nota contiene la confirmación de AMB-001, la fecha 2026-11-13 y el responsable Agent Sebaxtian. Las decisiones y parches anteriores no cambian. `python tools\sdd\validate.py --spec SPEC-005 --gate G4` devuelve `0`.
- **Evidencia (T-003, 2026-11-13, responsable Agent Sebaxtian):**
  - `specs/005-compuertas-completas/clarify.md` contiene «## Nota de confirmación (SPEC-006)» al final, línea 57. Confirma AMB-001: solo cuenta como superada una celda PASADO, con paréntesis de observación opcional; NO PASADO, PENDIENTE, PARCIAL y celdas compuestas con estado negativo son error.
  - Fecha: 2026-11-13 (UTC). Responsable: Agent Sebaxtian.
  - `python tools\sdd\validate.py --spec SPEC-005 --gate G4` → código `0`, `OK: sin hallazgos.`
- [x] Completada.

### T-004

- **Dependencias:** `T-001`, `T-002`, `T-003`.
- **Requisitos cubiertos:** `RNF-002`, `RNF-001`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 15 min.
- **Validación:** `Select-String -Path CHANGELOG.md -Pattern "SPEC-006"` encuentra una entrada bajo `## [Unreleased]`, antes de la primera versión publicada. La entrada cita las correcciones de §10, memoria operativa y clarificación de SPEC-005.
- **Evidencia (T-004, 2026-11-13):**
  - `Select-String -Path CHANGELOG.md -Pattern "SPEC-006"` → líneas 15, 16 y 17, bajo `## [Unreleased]` (línea 11) y antes de `## [v0.5.0] - 2026-11-13` (línea 19).
  - Bloque `### Changed` con tres entradas: §10 (`sdd` de solo lectura con bookkeeping limitado), memoria operativa (agentes y consulta de configuración) y clarificación de SPEC-005 (confirmación de AMB-001).
  - `git diff -- CHANGELOG.md`: 6 líneas añadidas, 0 eliminadas. No se han tocado `## [v0.5.0]` ni anteriores.
  - Finales de línea: 160 LF y 160 CRLF; termina en CRLF.
  - `python tools\sdd\validate.py --all` → código `0`. Única advertencia: `specs\006-observaciones-cierre\validation_report.md no existe`.
  - `git diff --check` → código `0`.
- [x] Completada.

### T-005

- **Dependencias:** `T-001`, `T-002`, `T-003`, `T-004`.
- **Requisitos cubiertos:** `RNF-001`, `RNF-003`, `CB-001`, `CB-002`.
- **Archivos:** ninguno. Solo lectura y ejecución de comandos.
- **Estimación:** 25 min.
- **Validación:** `python tools\sdd\validate.py --spec SPEC-006 --gate G2` y `python tools\sdd\validate.py --all` devuelven `0`. `python -m unittest discover -s tools\sdd\tests` ejecuta 47 pruebas con resultado `OK`. `git diff --name-only` lista solo `docs/sdd/PROTOCOLO_OPERATIVO.md`, `MEMORY.md`, `CHANGELOG.md`, `specs/005-compuertas-completas/clarify.md` y los archivos de `specs/006-observaciones-cierre/` y `specs/INDEX.md`. Cada archivo modificado conserva CRLF y salto final.
- **Reasignación registrada:** `tasks.md` asigna T-005 a `reviewer`. La ejecuta `coder` por decisión del orquestador, para no mezclar la regresión con la auditoría independiente posterior. La auditoría sigue siendo del `reviewer` (`validation_report.md`).
- **Evidencia (T-005, 2026-11-13):**
  - `python -m unittest discover -s tools\sdd\tests` → `Ran 47 tests`, `OK`, código `0`.
  - `python tools\sdd\validate.py --all` → código `0`. Única advertencia: `specs\006-observaciones-cierre\validation_report.md no existe`, que corresponde al `reviewer`.
  - `python tools\sdd\validate.py --spec SPEC-006 --gate G2` → código `0`, `OK: sin hallazgos.`.
  - `--spec SPEC-001 --gate G4`, `--spec SPEC-002 --gate G4 --git`, `--spec SPEC-003 --gate G4`, `--spec SPEC-004 --gate G4` y `--spec SPEC-005 --gate G4` → código `0` cada uno, `OK: sin hallazgos.`.
  - `git diff --check` → código `0`, sin hallazgos.
  - `git diff --name-only` → `CHANGELOG.md`, `MEMORY.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `specs/005-compuertas-completas/clarify.md`, `specs/INDEX.md`. Y `specs/006-observaciones-cierre/` como carpeta nueva sin seguimiento. Coincide con el alcance de T-005.
  - Finales de línea: `docs/sdd/PROTOCOLO_OPERATIVO.md` (168 LF, 168 CRLF), `MEMORY.md` (130/130), `CHANGELOG.md` (160/160) y `specs/005-compuertas-completas/clarify.md` (61/61). Los cuatro terminan en CRLF.
- [x] Completada.
