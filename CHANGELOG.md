# Changelog

Todos los cambios importantes del proyecto `LLaMA` se documentan en este archivo.

El formato sigue una estructura compatible con Semantic Versioning:

```text
vMAJOR.MINOR.PATCH
```

## [Unreleased]

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

## Historial de releases

Todavía no se ha publicado ningún release ni se ha creado ningún tag de versión.
