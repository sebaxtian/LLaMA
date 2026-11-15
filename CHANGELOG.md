# Changelog

Todos los cambios importantes del proyecto `LLaMA` se documentan en este archivo.

El formato sigue una estructura compatible con Semantic Versioning:

```text
vMAJOR.MINOR.PATCH
```

## [Unreleased]

## [v0.7.0] - 2026-11-14

### Added

- Informe de auditoría de cumplimiento SDD en `docs/sdd/auditoria_cumplimiento_sdd.md`: diez dimensiones evaluadas, 41 hallazgos con identificador `AUD-NNN`, hoja de ruta organizada en los bloques B1 a B4 y veredicto global `NO CONFORME` sobre el periodo de `SPEC-001` a `SPEC-007` (`SPEC-008`).
- Base normativa v2 (`SPEC-009`): mapa único de siete rangos, protocolo operativo redactado desde cero con sus dieciséis secciones, plantillas reconocidas como norma, contratos de informe analítico y de informe de auditoría, regla de versionado de specs, índice completo del corpus y lista `docs/sdd/firmantes_autorizados`. Fecha de corte `2026-11-14`.
- Rol `auditor` con lectura de la base completa y escritura limitada al informe que produce, implementado en `.opencode/agents/auditor.md` (`SPEC-011`).
- Integración continua en `.github/workflows/sdd.yml`: job `verify` que ejecuta la validación agregada y las dos suites de pruebas en cada Pull Request hacia `dev` y hacia `main`, con permiso de solo lectura y sin push, tag ni operación sobre el remoto (`SPEC-011`, `SPEC-014`).
- Comprobaciones nuevas del validador determinista: aprobación de G1, G4 y G6 contra `docs/sdd/firmantes_autorizados` y la firma del commit, cobertura de requisitos como error desde G2, detección de tareas abiertas en la ejecución agregada, G5 y G6 con lógica propia, transiciones e historial de transiciones, relación de sucesión y alcance exacto impreso en cada ejecución (`SPEC-010`).
- Trazabilidad profunda (`SPEC-012`): criterio de aceptación y evidencia obligatoria por tarea, sección de cierre de integración en el reporte de validación con el commit de integración y el tag del release, y regularización de `SPEC-001` a `SPEC-007` con esos campos.
- Informes `docs/sdd/auditoria_cierre_v0_7_0.md` y `docs/sdd/auditoria_final_v0_7_0.md`, con veredicto global `NO CONFORME` y `CONFORME CON OBSERVACIONES` respectivamente, y cierre registrado de las dieciséis observaciones de la reauditoría de cierre y de las cuatro observaciones que permanecían abiertas del informe final (`SPEC-013`, `SPEC-014`).
- Cierre de las observaciones de los informes de auditoría de conformidad, con identificadores `AUD-001` a `AUD-041` en la auditoría de origen y `AUD-038` a `AUD-102` en la reauditoría final (`SPEC-013`, `SPEC-014`).

### Changed

- Registro único de aprobaciones: G1 y G4 en `spec.md` y G6 en este archivo; el reporte de validación no porta casilla de aprobación y la aprobación se acredita por commit firmado con una clave de `docs/sdd/firmantes_autorizados` (`SPEC-009`).
- Ciclo de siete etapas con máquina de estados, escritor y evidencia por transición, y compuertas con una sola condición de entrada, una sola evidencia, un solo declarante y una sola verificación (`SPEC-010`).
- Matriz de permisos de los seis roles con tres reglas de precedencia declaradas; el orquestador queda con escritura en `.opencode/**` como única concesión, sin contradicción con §12 del protocolo operativo (`SPEC-011`, `SPEC-014`).
- Flujo Git alineado con la base v2: compuertas G5 y G6, eliminación de la rama de trabajo tras la integración, check `verify` exigible con `strict: true` en `main` y en `dev`, verificación de ancestría entre `main` y `dev` en lugar del conteo de commits y gramática de ramas que admite `docs/` (`SPEC-009`, `SPEC-013`).
- Documentos de la base sustituidos en sus mismas rutas: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `docs/sdd/plantillas/`; las versiones anteriores permanecen en el historial Git y el detalle consta en el Anexo de transición del protocolo (`SPEC-009`).
- Se archiva la rama `feat/gemma-4-26b-a4b-it-qat-gguf` sin integrarla: dos commits no integrados, permanece local, no se publica y no se fusiona (`SPEC-009`).
- Guías, informes de análisis e informes de auditoría declaran su carácter de referencia no normativa; el índice `docs/sdd/README.md` cubre la raíz del corpus, las plantillas y los informes, y el inventario de documentos normativos se calcula desde ese índice (`SPEC-009`, `SPEC-013`).

### Fixed

- El mecanismo de control deja de repartir el registro de G4 entre dos artefactos y de evaluar G4 antes de existir el reporte que la propia compuerta exige; los estados `implementing`, `implemented` y `validated` quedan con escritor declarado (`SPEC-010`).
- La cobertura `RF/CB → CA` deja de producir solo advertencia y pasa a error desde G2, y G5 y G6 dejan de compartir la verificación de G4 (`SPEC-010`).
- El job `verify` deja de ejecutar una sola suite: prepara el árbol con historial completo y con las etiquetas del repositorio y ejecuta `tools/sdd/tests` y `tools/git/tests` (`SPEC-014`).
- Se cierran las observaciones de la reauditoría de cierre: flujo con `actions/checkout` y `actions/setup-python`, comprobación de sincronización de release expresada como ancestría verificable, gramática de ramas que admite `docs/`, dos ventanas de legado declaradas y atribución corregida de la escritura de transiciones (`SPEC-013`).
- Se registran como cerradas las cuatro observaciones finales, con nota de cierre append-only en el reporte de `SPEC-013` que transcribe el veredicto del informe final sin alterar la matriz ni el dictamen (`SPEC-014`).

- Approved by: Agent Sebaxtian

## [v0.6.0] - 2026-11-13

### Added

- Herramientas deterministas de aprovisionamiento y verificación de protección de ramas en tools/git/ (configure_branch_protection.py y verify_branch_protection.py) y especificaciones declarativas JSON (tools/git/protection_rules/).
- Suite de pruebas unitarias (test_verify_branch_protection.py) y pruebas de rechazo deterministas en repositorio remoto (test_remote_rejection.py) para verificación de ramas protegidas.

### Changed

- Configuración remota de GitHub para sebaxtian/LLaMA: protección clásica estricta en ramas main y dev (PR obligatorio, enforce_admins, sin force push ni borrado) y desactivación de fusiones squash y rebase en favor exclusivo de merge --no-ff.
- Actualización normativa de docs/Flujo_de_Trabajo_Git.md, docs/sdd/PROTOCOLO_OPERATIVO.md, AGENTS.md y MEMORY.md: formalización de ramas auxiliares de empaquetado release/vX-Y-Z, actualización de gramática de ramas y erradicación de commits directos en dev.

- Approved by: Agent Sebaxtian

## [v0.5.1] - 2026-11-13

### Changed

- La tabla de agentes del protocolo describe a `sdd` como orquestador de solo lectura sobre artefactos y código, con bookkeeping Git limitado a artefactos de control (`SPEC-006`).
- La memoria operativa enumera los agentes del proyecto y documenta cómo consultar la configuración cargada (`SPEC-006`).
- La clarificación de SPEC-005 registra la confirmación del propietario sobre la regla de celda superada (`SPEC-006`).

- Approved by: Agent Sebaxtian

## [v0.5.0] - 2026-11-13

### Added

- La compuerta G3 verifica que todas las tareas estén marcadas como completadas (`SPEC-005`).
- La compuerta G4 evalúa el estado real de la matriz de trazabilidad, incluidas las celdas compuestas (`SPEC-005`).

### Changed

- La comprobación de rama con Git se omite en las specs publicadas, cuya rama ya se integró (`SPEC-005`).
- SPEC-001 declara en sus criterios de aceptación la cobertura de los requisitos (`SPEC-005`).
- El protocolo describe el bookkeeping Git de `sdd` limitado a artefactos de control (`SPEC-005`).

- Approved by: Agent Sebaxtian

## [v0.4.0] - 2026-11-13

### Added

- Subagente `documenter` para correcciones editoriales y normativas en `docs/` y `AGENTS.md`, con permiso de edición acotado y sin terminal (`SPEC-004`).

### Changed

- G4 se describe como aprobación de la implementación validada en el protocolo operativo y en `AGENTS.md` (`SPEC-004`).
- El commit de release puede registrar `CHANGELOG.md`, `specs/INDEX.md` y el frontmatter de la spec del release (`SPEC-004`).
- Se documenta el criterio de incremento cuando un release combina correcciones con adiciones derivadas de ellas (`SPEC-004`).

- Approved by: Agent Sebaxtian

## [v0.3.1] - 2026-11-13

### Added

- Validación estricta de la compuerta G4 en `tools/sdd/validate.py`: dictamen por casilla marcada, filas no superadas y reporte obligatorio con G4, G5, G6 o estado validado (`SPEC-003`).
- Advertencia de cobertura `RF/CB → CA` mediante las líneas `Cubre:` de los criterios de aceptación (`SPEC-003`).

### Fixed

- La compuerta G4 ya no acepta «NO CONVERGIDO» como convergencia (`SPEC-003`).
- La detección de filas FALLADO o NO PASADO ahora evalúa las celdas reales de la matriz (`SPEC-003`).

- Approved by: Agent Sebaxtian

## [v0.3.0] - 2026-11-13

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

- Approved by: Agent Sebaxtian

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

Se publicó `v0.1.0` como primera versión estructural y documental del proyecto. El historial de releases con su fecha UTC y su tag anotado es:

| Versión | Fecha | Tag |
|---|---|---|
| `v0.1.0` | 2026-11-10 | `v0.1.0` |
| `v0.2.0` | 2026-11-12 | `v0.2.0` |
| `v0.3.0` | 2026-11-13 | `v0.3.0` |
| `v0.3.1` | 2026-11-13 | `v0.3.1` |
| `v0.4.0` | 2026-11-13 | `v0.4.0` |
| `v0.5.0` | 2026-11-13 | `v0.5.0` |
| `v0.5.1` | 2026-11-13 | `v0.5.1` |
| `v0.6.0` | 2026-11-13 | `v0.6.0` |
| `v0.7.0` | 2026-11-14 | `v0.7.0` |

El empaquetado de `v0.7.0` queda registrado en su entrada y en la tabla anterior; G6 permanece pendiente de la línea `- Approved by: Agent Sebaxtian` que el propietario introducirá en un commit firmado al publicar, y el tag `v0.7.0` se crea sobre el commit publicado.
