# Plan técnico - SPEC-002

## Referencias

- `spec.md`: `SPEC-002`.
- `clarify.md`: `SPEC-002`.
- `docs/sdd/PROTOCOLO_OPERATIVO.md` §10 (agentes y permisos) y §9 (validador determinista).
- `docs/sdd/guia_subagentes_opencode_sdd.md` §7 (modo `subagent` obligatorio para delegar).

## Arquitectura de módulos

La feature no introduce código ejecutable. Ajusta tres definiciones de agentes en `.opencode/agents/`:

1. `planner.md`: cambia `mode` de `primary` a `all` y explicita en `description` que es invocable por `sdd`.
2. `coder.md`: mismo cambio de `mode` y de `description`.
3. `sdd.md`: añade reglas `subagent` explícitas, una regla `shell` acotada al validador y una sección operativa de orquestación.

`reviewer.md` no se modifica: ya es `mode: subagent` y solo escribe `specs/*/validation_report.md`.

## Esquemas, tipos e interfaces

- Frontmatter YAML con `description`, `mode` y `permissions`.
- `mode`: `primary`, `subagent` o `all`.
- Cada regla de `permissions` usa `action`, `resource` y `effect`.
- Valores de `action` usados: `edit`, `subagent`, `shell`.
- Valores de `effect` usados: `deny`, `allow`.
- Interfaz de delegación: herramienta `subagent` con `agent`, `description` y `prompt`.

## Decisiones técnicas

### DEC-001

- **Decisión:** usar `mode: all` en `planner` y `coder`.
- **Alternativas descartadas:** `mode: subagent` rompería los comandos `sdd-spec`, `sdd-clarify`, `sdd-plan`, `sdd-tasks` y `sdd-implement`, que declaran `agent: planner` y `agent: coder`.
- **Motivo:** cubre RF-002, RF-003 y CA-006 sin regresiones.

### DEC-002

- **Decisión:** declarar `subagent` con `deny *` primero y `allow` por agente después.
- **Alternativas descartadas:** confiar en la política base (`allow *`) no expresa RF-004 ni deja rastro del mínimo privilegio.
- **Motivo:** en OpenCode V2 gana la última regla coincidente; el orden produce una lista blanca efectiva.

### DEC-003

- **Decisión:** permitir `shell` solo con el patrón `python tools\sdd\validate.py *`.
- **Alternativas descartadas:** permitir `shell *` ampliaría el privilegio del orquestador sin necesidad.
- **Motivo:** `sdd` necesita el validador para verificar compuertas (RF-006).

### DEC-004

- **Decisión:** documentar plantillas de prompt autosuficientes por subagente.
- **Alternativas descartadas:** delegar con referencias al historial de la conversación, que el subagente no recibe.
- **Motivo:** los subagentes arrancan con contexto nuevo; cubre RF-007 y CB-002.

### DEC-005

- **Decisión:** no modificar `opencode.jsonc` ni `reviewer.md`.
- **Alternativas descartadas:** mover los permisos de agentes a la configuración global; mezclaría alcances y dificultaría la auditoría.
- **Motivo:** mantiene el cambio en el mínimo conjunto de archivos declarado en `spec.md`.

## Estrategia de testing

- Validación determinista: `python tools\sdd\validate.py --all` y `--spec SPEC-002 --gate G4`.
- Inspección de frontmatter: confirmar `mode: all` en `planner` y `coder`, y las reglas `subagent`/`shell` en `sdd`.
- Prueba manual en la TUI: abrir el agente `sdd` y comprobar que `planner`, `coder`, `reviewer` y `explore` aparecen como subagentes disponibles.
- Prueba negativa manual: intentar editar un archivo desde `sdd` y confirmar la denegación.
- Higiene de integración: `git diff --check` y `git status --short`.

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | `sdd.md` reglas `subagent` | `planner` y `coder` disponibles en la TUI |
| RF-002 | `planner.md` `mode: all` | inspección de frontmatter |
| RF-003 | `coder.md` `mode: all` | inspección de frontmatter |
| RF-004 | `subagent deny *` | intento de lanzar agente no autorizado |
| RF-005 | `edit deny *` en `sdd.md` | intento de edición denegado |
| RF-006 | sección de orquestación | compuerta previa verificada antes del lanzamiento |
| RF-007 | plantillas de prompt | revisión del prompt con spec, etapa y salida |
| RNF-001 | `permissions` ordenado | inspección de frontmatter |
| RNF-002 | `CHANGELOG.md` | entrada en `Unreleased` |
| CB-001 | sección de orquestación | regla explícita de G4 previa |
| CB-002 | sección de orquestación | regla de bloqueo registrado |
| CB-003 | sección de orquestación | regla de parada por error del validador |