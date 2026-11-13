# Changelog

Todos los cambios importantes del proyecto `LLaMA` se documentan en este archivo.

El formato sigue una estructura compatible con Semantic Versioning:

```text
vMAJOR.MINOR.PATCH
```

## [Unreleased]

### Added

- Delegación del ciclo SDD desde el agente `sdd` hacia los subagentes `planner`, `coder`, `reviewer` y `explore` (`SPEC-002`).
- Sección de orquestación en `.opencode/agents/sdd.md` con tabla etapa-subagente, plantillas de solicitud y reglas de compuerta.

### Changed

- `planner` y `coder` usan `mode: all` para ejecutarse como agentes primarios y como subagentes (`SPEC-002`).
- `sdd` aplica una lista blanca de subagentes: `planner`, `coder`, `reviewer` y `explore`; el resto queda denegado (`SPEC-002`).
- `sdd` acota los comandos de shell con una regla general `ask` y una lista blanca: validador determinista, git de lectura, `git add` y `git commit` (`SPEC-002`).
- `planner` y `coder` deniegan el lanzamiento de subagentes (`SPEC-002`).

### Fixed

- La tabla de compuertas de `.opencode/agents/sdd.md` se alinea con `docs/sdd/PROTOCOLO_OPERATIVO.md` §2: Implement se verifica con G2 y G4 queda al final de Validate (`SPEC-002`).
- Se añaden los criterios de aceptación CA-007 a CA-010 y se alinea CB-001 a G2 (`SPEC-002`).

## [v0.2.0] - 2026-11-12

### Added

- Configuración del proveedor local `LLaMA` en `opencode.jsonc` mediante la API compatible con OpenAI de llama.cpp.
- Metodología de Desarrollo Basado en Especificaciones (SDD) Spec-Anchored para el proyecto.
- `docs/constitution.md` como norma suprema del proyecto.
- `docs/sdd/PROTOCOLO_OPERATIVO.md` como norma SDD ejecutable (7 etapas, compuertas G1–G6, gramática de IDs, EARS).
- Corpus de referencia SDD versionado en `docs/sdd/` con índice en `docs/sdd/README.md`.
- Plantillas de artefactos SDD en `docs/sdd/plantillas/` (spec, clarify, plan, tasks, validation_report).
- `specs/INDEX.md` como registro canónico de especificaciones.
- Validador determinista `tools/sdd/validate.py`, envoltorio `validate.bat` y pruebas `unittest`.
- Agentes OpenCode `sdd`, `planner`, `coder` y `reviewer` en `.opencode/agents/`.
- Comandos `/sdd-spec`, `/sdd-clarify`, `/sdd-plan`, `/sdd-tasks`, `/sdd-implement`, `/sdd-validate`, `/sdd-status` y `/sdd-check`.
- Skills `sdd-lifecycle`, `ears-spec`, `sdd-plan-tasks`, `tdd-implement` y `llama-validation`.
- Normalización del corpus `docs/sdd/` (sufijo `-mcp`, IDs de 3 dígitos, rutas `specs/NNN-slug/`, `validation_report.md`).

- `main.bat` como menú raíz que descubre y ejecuta los scripts de `src/` (piloto `SPEC-001`).

### Changed

- Se actualizó `default_agent` a `plan` en `opencode.jsonc`.
- Se reescribió `AGENTS.md` para condensarlo en 30–70 líneas y alinearlo con la jerarquía normativa.
- Se añadieron permisos en `opencode.jsonc`: deny de edición en `bin/` y `models/`, y `ask` para `git push` y `git tag`.
- Se integraron las compuertas SDD (G5/G6) y las excepciones de bootstrap y editorial en `docs/Flujo_de_Trabajo_Git.md`.
- Se actualizaron `README.md` y `MEMORY.md` con la metodología SDD y la nueva estructura.

- Approved by: Agent Sebaxtian

## [v0.1.0] - 2026-11-10

### Added

- Servidor MCP remoto oficial de GitHub con toolsets limitados para contexto, repositorios, issues y pull requests.
- `example.env` como plantilla para `GITHUB_PERSONAL_ACCESS_TOKEN` sin credenciales reales.
- `opencode.jsonc` con configuración de proyecto, contexto operativo y protección de `llama.cpp/`.
- Estructura inicial del proyecto para ejecutar modelos LLM localmente con llama.cpp.
- Documentación de la arquitectura local y los benchmarks iniciales.
- `AGENTS.md` con las reglas operativas para agentes.
- `MEMORY.md` con la memoria operativa del proyecto.
- `README.md` con la guía general, arquitectura y flujo de trabajo.
- `LICENSE` con licencia MIT para el material propio del proyecto.
- `.gitignore` para excluir modelos, binarios, dependencias y el repositorio externo `llama.cpp`.
- Archivos `.gitkeep` para conservar inicializadas las carpetas `bin/`, `models/` y `src/`.
- Documento `docs/Flujo_de_Trabajo_Git.md` con la estrategia de ramas, releases y tags.

### Changed

- Se definió el flujo de trabajo basado en las ramas `main`, `dev`, `feat/*`, `fix/*` y `hotfix/*`.
- Se configuró la conservación explícita de `models/.gitkeep` en `.gitignore`.
- Se formalizó la estrategia de integración mediante `merge --no-ff`, sin rebase ni squash.
- Se definieron el bootstrap determinista de `main` y `dev`, la gramática de ramas y la política exacta de tags anotados.
- Se añadieron exclusiones para logs, resultados y archivos temporales locales.
- Se añadió la convención de nombres MCP con el sufijo `-mcp` y la exclusión de configuración local de `.vscode/`.
- Se actualizó la documentación operativa para distinguir la línea base normativa del flujo Git frente al estado histórico del repositorio.
- Se documentaron en `AGENTS.md`, `README.md` y `MEMORY.md` la configuración de `github-mcp`, el uso de `example.env` y la protección de credenciales locales.
- Se formalizó el procedimiento obligatorio de hotfix, resolución de conflictos, validación de tags y publicación de releases.
- Se definieron la gramática exacta de tags, el formato UTC del changelog y la regla para una sección `Unreleased` vacía.
- Se formalizaron la protección de `main` y `dev`, las validaciones por tipo de cambio y el registro obligatorio de autorización de releases.
- Se autorizó explícitamente el commit de preparación de release en `dev` como excepción exclusiva para actualizar `CHANGELOG.md`.
- Se actualizó el documento maestro con los benchmarks de Phi-4, Codestral 22B, Gemma-2-27B y Qwen2.5-Coder-32B, las matrices LM Studio/llama.cpp, el catálogo de modelos, los estados de validación y las configuraciones propuestas para la RTX 5060 Ti de 16 GB sobre USB4.
- Se sincronizó la documentación del estado Git actual y se creó `feat/sync-git-state` desde `dev`; la rama fue validada e integrada en `dev` mediante `merge --no-ff`.

### Fixed

- Se corrigió la exclusión accidental de `models/.gitkeep` para permitir que la carpeta `models/` permanezca inicializada en los clones.

### Removed

### Security

- Se excluye `/.env` de Git y se deniega a OpenCode su lectura y edición.

- Approved by: Agent Sebaxtian

## Historial de releases

Se publicó `v0.1.0` como primera versión estructural y documental del proyecto.
