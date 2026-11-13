# Tareas - SPEC-002

## Progreso

- [x] 5 de 5 tareas completadas.

## Tareas

### T-001

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-002`.
- **Archivos:** `.opencode/agents/planner.md`.
- **Estimación:** 15 min.
- **Validación:** el frontmatter declara `mode: all` y la `description` indica que es invocable por `sdd`.
- [x] Completada.

### T-002

- **Dependencias:** ninguna.
- **Requisitos cubiertos:** `RF-003`.
- **Archivos:** `.opencode/agents/coder.md`.
- **Estimación:** 15 min.
- **Validación:** el frontmatter declara `mode: all` y la `description` indica que es invocable por `sdd`.
- [x] Completada.

### T-003

- **Dependencias:** `T-001`, `T-002`.
- **Requisitos cubiertos:** `RF-001`, `RF-004`, `RF-005`, `RNF-001`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 20 min.
- **Validación:** el frontmatter conserva `edit deny *` y añade `subagent deny *` seguido de `allow` para `planner`, `coder`, `reviewer` y `explore`.
- [x] Completada.

### T-004

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RF-006`, `RF-007`, `CB-001`, `CB-002`, `CB-003`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 25 min.
- **Validación:** el cuerpo documenta tabla etapa-subagente, plantillas de prompt con spec, etapa y salida esperada, y la parada ante compuerta no aprobada, ambigüedad o error del validador.
- [x] Completada.

### T-005

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RNF-002`.
- **Archivos:** `specs/INDEX.md`, `CHANGELOG.md`, `specs/002-orquestacion-subagentes-sdd/tasks.md`, `specs/002-orquestacion-subagentes-sdd/spec.md`.
- **Estimación:** 20 min.
- **Validación:** `python tools\sdd\validate.py --all` devuelve código 0 y `git diff --check` no reporta problemas.
- [x] Completada.

## Evidencia

- `opencode api get '/api/agent?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` devuelve `coder | all`, `planner | all`, `reviewer | subagent` y `sdd | primary`: OpenCode cargó la configuración y publica los agentes con el modo esperado.
- `opencode api get '/api/agent/sdd?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` devuelve los permisos efectivos: `edit *` deny, `subagent *` deny seguido de `allow` para `planner`, `coder`, `reviewer` y `explore`, y `shell` acotado a `python tools\sdd\validate.py *`.
- `python tools\sdd\validate.py --spec SPEC-002 --gate G2` devuelve `OK: sin hallazgos.`
- `python tools\sdd\validate.py --all` devuelve código 0.
- `git diff --check` sin hallazgos; `git status --short` solo muestra los archivos declarados en las tareas.