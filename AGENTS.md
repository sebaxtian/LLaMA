# Instrucciones del proyecto LLaMA

Reglas operativas para agentes. La norma suprema es `docs/constitution.md`; el procedimiento SDD es `docs/sdd/PROTOCOLO_OPERATIVO.md`; el flujo Git es `docs/Flujo_de_Trabajo_Git.md`. Ante contradicción, prevalece el documento de mayor rango y se detiene el trabajo.

## Alcance

- Repositorio para ejecutar y probar modelos LLM localmente con llama.cpp en Windows 11.
- `src/`: scripts `.bat` por modelo (versionables). `models/`: modelos (no versionados). `bin/`: dependencias y binarios de llama.cpp (no versionados).
- `docs/`: documentación técnica y de proceso. `MEMORY.md`: contexto operativo. `CHANGELOG.md`: historial y releases.

## Desarrollo (SDD)

- Toda feature, fix, refactor o cambio de configuración exige una spec aprobada (`specs/NNN-slug/`).
- Ciclo de 7 etapas: Specify → Clarify → Plan → Tasks → Implement (TDD) → Validate.
- Identificadores: `SPEC-001`, `RF-001`, `RNF-001`, `CB-001`, `AMB-001`, `CA-001`, `T-001`, `DEC-001`.
- Requisitos en notación EARS. Trazabilidad obligatoria `RF/CB → CA → T → evidencia`.
- Aprobaciones humanas en G1 (spec), G4 (implementación) y G6 (release), registradas como `- Approved by: Agent Sebaxtian`.
- Prohibida la autoaprobación. Un agente no modifica requisitos para ajustarlos al código.
- Excepción sin spec: solo cambios exclusivamente editoriales (commit `docs:` o `chore:`).

## Guardrails no negociables

- `llama.cpp/`: repositorio oficial. Prohibido crear, modificar, eliminar, mover, renombrar o sobrescribir nada en su interior. Solo lectura de referencia.
- `bin/`: sin modelos dentro. `models/`: sin binarios dentro. `.env`: protegido contra lectura y edición.
- Conservar `.gitkeep` de `bin/`, `models/` y `src/`.

## Ejecución local

- Los `.bat` resuelven la raíz con `%~dp0`; no dependen del directorio actual ni del `PATH`.
- Seleccionar explícitamente el ejecutable de llama.cpp y el `.gguf`; verificar que ambos existan antes de ejecutar.
- Mantener separados los binarios precompilados de `bin/` de los artefactos de compilación.

## Hardware objetivo

- GPU NVIDIA RTX 5060 Ti (16 GB VRAM, eGPU USB4); RAM ~32 GB; CPU Intel i9 13.ª gen.
- Parámetros iniciales: `-ngl 99`, `-lm none`; modelos ≥20B con `-np 1`; 10B–15B con `-c 8192`; 20B–24B validar VRAM; 25B–28B con `-c 4096 -np 1` y `-fa off` en Gemma; 30B–35B con cuantización Q3, `-c 4096`, `-np 1`.
- No declarar un modelo optimizado sin comprobar carga, VRAM/RAM y velocidad.

## Git

- Ramas `feat/*`, `fix/*`, `hotfix/*` en minúsculas, números y guiones. Integración solo con `merge --no-ff`.
- Sin rebase ni squash. Tags anotados `vMAJOR.MINOR.PATCH` con mensaje `Release vX.Y.Z`.
- `main` y `dev` protegidas por política; no se trabaja directamente sobre ellas.
- Commits de implementación referencian `Spec: SPEC-NNN` en el cuerpo.
- Registrar cambios en `CHANGELOG.md` bajo `Unreleased` hasta publicar release.

## Validación

- Antes de integrar: `git diff --check`, `git status --short`, revisar alcance y ejecutar `python tools\sdd\validate.py --all`.
- No incorporar modelos, binarios, dependencias, credenciales ni contenido de `llama.cpp/` al repositorio.
- Un script se considera validado solo si se ejecuta correctamente con el modelo configurado; `llama-bench` no sustituye la validación de un servidor con contexto largo.

## MCP y secretos

- Servidores MCP con sufijo `-mcp` (ej. `github-mcp`). Referencias a herramientas como `github-mcp_*`.
- Sin tokens ni credenciales en archivos versionables; usar `example.env` como plantilla.

## Referencias

- `docs/constitution.md` (norma suprema) y `docs/sdd/PROTOCOLO_OPERATIVO.md` (SDD).
- `docs/sdd/README.md` (índice del corpus) y `docs/Flujo_de_Trabajo_Git.md` (Git).
