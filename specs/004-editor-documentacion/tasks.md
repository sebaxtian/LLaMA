# Tareas — SPEC-004

## Progreso

- [x] 5 de 5 tareas completadas.

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-002`, `RF-003`, `RF-005`, `RNF-001`, `RNF-003`, `CB-001`, `CB-002`, `CB-003`.
- **Archivos:** `.opencode/agents/documenter.md`.
- **Estimación:** 25 min.
- **Validación:** `Select-String -Path .opencode/agents/documenter.md -Pattern '^mode: subagent$'` devuelve una coincidencia; la lista de permisos sigue el orden de DEC-001 (denegaciones generales de edición, de shell y de subagentes antes de las excepciones de `docs/**` y `AGENTS.md`); la lista efectiva incluye `shell *` deny (AMB-006); el cuerpo contiene la regla de parada de CB-001 y la conservación de CRLF.
- [x] Completada.
- **Evidencia (2026-11-13):**
  - Archivo creado `.opencode/agents/documenter.md` (1497 bytes), UTF-8 sin BOM, CRLF en todas las líneas y salto final; sin LF desnudos.
  - Frontmatter en el orden de DEC-001 con AMB-006: `edit *` deny, `shell *` deny, `subagent *` deny, `docs/**` allow, `AGENTS.md` allow. `mode: subagent`.
  - Autorización de escritura en `.opencode/agents/`: AMB-005 y DEC-006 (`clarify.md`, `plan.md`).
  - `Select-String -Path .opencode/agents/documenter.md -Pattern '^mode: subagent$'`: 1 coincidencia (línea 3).
  - `opencode api get '/api/agent?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'`: lista `documenter` con `mode: subagent`.
  - `opencode api get '/api/agent/documenter?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'`: reglas efectivas en orden `edit *` deny, `shell *` deny, `subagent *` deny, `edit docs/**` allow, `edit AGENTS.md` allow.
  - `python tools\sdd\validate.py --all`: código de salida 0. Avisos preexistentes en `specs/001-main-menu/spec.md` (RF sin «Cubre:») y `specs/004-editor-documentacion/validation_report.md` (aún no existe, esperado en esta etapa).
  - `git diff --check`: código 0.
  - Tarea ejecutada por `coder` con excepción AMB-005 / DEC-006.

### T-002

- **Dependencias:** `T-001`.
- **Requisitos cubiertos:** `RF-001`, `RF-004`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 20 min.
- **Validación:** `Select-String -Path .opencode/agents/sdd.md -Pattern 'documenter'` devuelve al menos dos coincidencias (regla de permiso y orquestación); `Select-String -Path .opencode/agents/sdd.md -Pattern 'Resultado esperado'` devuelve la interfaz de solicitud de `documenter` con «Etapa:» (AMB-004).
- [x] Completada.
- **Evidencia (2026-11-13):**
  - Frontmatter de `.opencode/agents/sdd.md`: añadido `subagent documenter allow` justo después de `subagent explore allow`. Diff de 3 líneas insertadas, sin otros cambios. CRLF y salto final conservados.
  - `opencode api get '/api/agent/sdd?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'`: `subagent *` deny, seguido de allow para `planner`, `coder`, `reviewer`, `explore` y `documenter`.
  - `opencode api get '/api/agent?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'`: `sdd` en `mode: primary`; `documenter` en `mode: subagent`.
  - `python tools\sdd\validate.py --all`: código 0 (mismos avisos preexistentes que en T-001).
  - Cuerpo de `sdd.md` (opción A autorizada por el propietario): la lista de funciones enumera `documenter`; se añade la plantilla «**Documenter:**» con «Etapa: document» en «### Solicitudes». Tabla de etapas, reglas de orquestación y frontmatter sin cambios.
  - `Select-String -Path .opencode/agents/sdd.md -Pattern 'documenter'`: 3 coincidencias (línea 24, regla de permiso; línea 74, lista de funciones de orquestación; línea 99, plantilla de solicitud).
  - `Select-String -Path .opencode/agents/sdd.md -Pattern 'Etapa: document'`: 1 coincidencia (línea 99).
  - `opencode api get '/api/agent/sdd?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` tras la opción A: `subagent *` deny seguido de allow para `planner`, `coder`, `reviewer`, `explore` y `documenter`.
  - `git diff --check`: código 0. `sdd.md` y `tasks.md` mantienen CRLF y salto final.

### T-003

- **Dependencias:** `T-001`, `T-002`.
- **Requisitos cubiertos:** `RF-005`, `RF-006`, `RNF-003`, `CB-001`.
- **Archivos:** `docs/sdd/PROTOCOLO_OPERATIVO.md`, `AGENTS.md`, `docs/Flujo_de_Trabajo_Git.md`.
- **Estimación:** 30 min.
- **Validación:** `Select-String -Path docs/sdd/PROTOCOLO_OPERATIVO.md -Pattern 'aprueba la implementación validada'` devuelve una coincidencia; `Select-String -Path AGENTS.md -Pattern 'G4 \(implementación validada\)'` devuelve una coincidencia; `Select-String -Path docs/Flujo_de_Trabajo_Git.md -Pattern 'specs/INDEX.md'` devuelve al menos una coincidencia en la sección de release; `git diff --check` no reporta errores; cada archivo editado conserva CRLF y salto final.
- [x] Completada.
- **Evidencia (2026-11-13, verificada por la sesión orquestadora):**
  - `git diff --stat` (docs y AGENTS.md): `AGENTS.md` (-1/+1), `docs/Flujo_de_Trabajo_Git.md` (+2/-1), `docs/sdd/PROTOCOLO_OPERATIVO.md` (+2/-1).
  - Cinco ediciones presentes: G4 en §6 de `PROTOCOLO_OPERATIVO.md` («G4: el propietario aprueba la implementación validada (`validation_report.md` al 100 %)»); fila de `documenter` en la tabla §10; «G4 (implementación validada)» en `AGENTS.md`; excepción de contabilidad del commit `chore: prepare release` en `Flujo_de_Trabajo_Git.md` (`CHANGELOG.md`, `specs/INDEX.md` y frontmatter de la spec); criterio de incremento SemVer para releases mixtos en `Flujo_de_Trabajo_Git.md`.
  - `git diff --check`: código 0.
  - `python tools\sdd\validate.py --all`: código 0.
  - Ejecutada por `documenter` (`.opencode/agents/documenter.md`).
  - Corrección BRE-01: el bloque de procedimiento de release de `docs/Flujo_de_Trabajo_Git.md` incluye `specs/NNN-slug/spec.md` en el `git add`, junto a `CHANGELOG.md` y `specs/INDEX.md` (`git add CHANGELOG.md specs/INDEX.md specs/NNN-slug/spec.md`).
  - Corrección BRE-02: la fila de `documenter` en la tabla §10 de `docs/sdd/PROTOCOLO_OPERATIVO.md` fue ratificada por el propietario el 2026-11-13 (AMB-007).

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RNF-002`.
- **Archivos:** `CHANGELOG.md`.
- **Estimación:** 15 min.
- **Validación:** `Select-String -Path CHANGELOG.md -Pattern 'SPEC-004'` devuelve una coincidencia situada entre `## [Unreleased]` y la siguiente sección de versión; `git diff --check` no reporta errores.
- [x] Completada.
- **Evidencia (2026-11-13):**
  - `git diff -- CHANGELOG.md`: solo añade, bajo `## [Unreleased]`, las secciones `### Added` (1 entrada) y `### Changed` (3 entradas), todas con `(SPEC-004)`. No se modifica `## [v0.3.1]` ni anteriores.
  - Coincidencias de `SPEC-004` en `CHANGELOG.md`: 4, todas entre `## [Unreleased]` y `## [v0.3.1]`.
  - `git diff --check`: código 0.
  - `python tools\sdd\validate.py --all`: código 0 (avisos preexistentes en `specs/001-main-menu/spec.md` y `validation_report.md` aún inexistente).
  - `CHANGELOG.md` mantiene CRLF y salto final.

### T-005

- **Dependencias:** `T-001`, `T-002`, `T-003`, `T-004`.
- **Requisitos cubiertos:** `RF-001`, `RF-002`, `RF-003`, `RF-004`, `RNF-001`, `CB-002`, `CB-003`.
- **Archivos:** `specs/004-editor-documentacion/**` (artefactos de la propia spec), `specs/INDEX.md` (fila de registro) y, en solo lectura, los declarados en T-001 a T-004.
- **Estimación:** 30 min.
- **Validación:** `opencode api get /api/agent/documenter` (desde la raíz del repositorio) muestra `mode: subagent`, con permisos en el orden de DEC-001; `opencode api get /api/agent/sdd` muestra la regla de `documenter`; las reglas efectivas de `documenter` permiten `docs/**` y `AGENTS.md` y deniegan el resto de la edición y el lanzamiento de subagentes; `python tools\sdd\validate.py --spec SPEC-004 --gate G2` y `python tools\sdd\validate.py --all` salen con código `0`; `git status --short` no muestra cambios fuera de los archivos declarados. Si el endpoint no lista los agentes del repositorio, la tarea queda BLOQUEADA y no se marca como completada (DEC-005).
- [x] Completada.
- **Evidencia de verificación final (2026-11-13):**
  1. `opencode api get '/api/agent?location[directory]=…LLaMA'`: `documenter` con `mode: subagent`; `sdd` con `mode: primary`.
  2. `opencode api get '/api/agent/documenter?location[directory]=…LLaMA'`: `edit *` deny, `shell *` deny, `subagent *` deny, `edit docs/**` allow, `edit AGENTS.md` allow. No hay ninguna regla allow para `specs/`, `src/`, `tools/` ni `.opencode/`. Nota: la respuesta incluye una base `*` allow previa; el orden es el que aplica, porque la última regla coincidente gana.
  3. `opencode api get '/api/agent/sdd?location[directory]=…LLaMA'`: `subagent *` deny, seguido de allow para `planner`, `coder`, `reviewer`, `explore` y `documenter`.
  4. `python tools\sdd\validate.py --all`: código 0.
  5. `git diff --check`: código 0.
  6. Formato CRLF y salto final (conteo de LF desnudos = 0): `.opencode/agents/documenter.md`, `.opencode/agents/sdd.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, `CHANGELOG.md`.
  - Validación adicional de `tasks.md`: `python tools\sdd\validate.py --spec SPEC-004 --gate G2`: código 0.
  - **Alcance declarado:** los cuatro artefactos de la spec (`spec.md`, `clarify.md`, `plan.md`, `tasks.md`) y la fila de registro de `specs/INDEX.md` son artefactos de las etapas 2 a 5 (Specify, Clarify, Plan y Tasks), no archivos de implementación. Por eso se declaran en el alcance de esta tarea de verificación (`specs/004-editor-documentacion/**` y `specs/INDEX.md`).
  - **Deuda del validador:** `python tools\sdd\validate.py --gate G3` no comprueba que las tareas estén marcadas `[x]`. Su código 0 no verifica la completitud de T-005 ni de ninguna otra tarea. Queda como deuda del validador, fuera del alcance de esta spec.
- **Hallazgo bloqueante:** `git status --short` muestra `M specs/INDEX.md`, que no está declarado en el campo `Archivos` de ninguna tarea de SPEC-004. Es el registro de estado de SPEC-004 previsto en `plan.md` (arquitectura, línea 17) y ya existía antes de T-001. El criterio de T-005 exige que no haya cambios fuera de los archivos declarados, así que la tarea no puede marcarse como completada. Requiere decisión del propietario: declarar `specs/INDEX.md` en T-005 (o en una tarea de registro) o registrar el cambio en un commit separado. No he modificado `tasks.md` en el campo `Archivos`, porque eso exige actualización explícita del propietario.
- **Resolución de la opción A (2026-11-13):** `specs/INDEX.md` añadido al campo `Archivos` de T-005 como fila de registro de SPEC-004 creada en la etapa Specify.
- **Estado de `git status --short -uall`:** `M` en `.opencode/agents/sdd.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/Flujo_de_Trabajo_Git.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` y `specs/INDEX.md`; `??` en `.opencode/agents/documenter.md` y en `specs/004-editor-documentacion/{spec,clarify,plan,tasks}.md`. Los seis primeros están declarados en T-001 a T-005. **Los cuatro artefactos de la spec no están declarados en ningún campo `Archivos`.** Por eso no puede afirmarse que `git status` quede limitado a los archivos declarados.
- **Hallazgo sobre el validador:** `python tools\sdd\validate.py --spec SPEC-004 --gate G3` devuelve 0, pero el validador solo comprueba los requisitos de G1 y G2 y no verifica que todas las tareas estén marcadas `[x]`. Su código 0 no prueba que T-005 esté completa.
- **Decisión del propietario (2026-11-13):** se cierra con alcance explícito. Los artefactos de la spec y la fila de `specs/INDEX.md` se declaran en el campo `Archivos` de T-005; T-005 queda completada con esa excepción registrada.
