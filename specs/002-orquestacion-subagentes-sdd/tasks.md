# Tareas - SPEC-002

## Progreso

- [x] 8 de 8 tareas completadas.

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

### T-006

- **Dependencias:** `T-003`.
- **Requisitos cubiertos:** `RNF-001`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 20 min.
- **Validación:** la lista cargada en `/api/agent/sdd` muestra la regla general `shell *` con efecto `ask` antes del `allow` del validador y antes de la lista blanca de solo lectura (`git status *`, `git diff *`, `git log *`, `git show *`, `git branch *`, `git rev-parse *`); merge, tag y push permanecen en `ask`.
- [x] Completada.

### T-007

- **Dependencias:** `T-004`.
- **Requisitos cubiertos:** `RF-006`, `CB-001`, `CB-003`.
- **Archivos:** `.opencode/agents/sdd.md`.
- **Estimación:** 25 min.
- **Validación:** la tabla «Etapa, subagente y precondición» declara en la fila 3 Clarify «rama `feat/*` y spec en `draft`», en la fila 4 Plan «G1 aprobada y spec en `clarified`» y en la fila 6 Implement «G2 aprobada y spec en `tasked`»; la regla 2 dice «No lances `coder` sin G2 aprobada; no lances `reviewer` sin G3 completa»; el contraste con PROTOCOLO §2 no presenta contradicción.
- [x] Completada.

### T-008

- **Dependencias:** `T-001`, `T-002`.
- **Requisitos cubiertos:** `RNF-001`.
- **Archivos:** `.opencode/agents/planner.md`, `.opencode/agents/coder.md`.
- **Estimación:** 15 min.
- **Validación:** `/api/agent` muestra `subagent *` con efecto `deny` en las listas de permisos de `planner` y de `coder`.
- [x] Completada.

## Evidencia

- `opencode api get '/api/agent?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` devuelve `coder | all`, `planner | all`, `reviewer | subagent` y `sdd | primary`: OpenCode cargó la configuración y publica los agentes con el modo esperado.
- `opencode api get '/api/agent/sdd?location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA'` devuelve los permisos efectivos: `edit *` deny, `subagent *` deny seguido de `allow` para `planner`, `coder`, `reviewer` y `explore`, y `shell` acotado a `python tools\sdd\validate.py *` (estado previo a T-006; tras T-006 el permiso se acota con `shell *` en `ask` más la lista blanca registrada en la evidencia de T-006).
- `python tools\sdd\validate.py --spec SPEC-002 --gate G2` devuelve `OK: sin hallazgos.`
- `python tools\sdd\validate.py --all` devuelve código 0.
- `git diff --check` sin hallazgos; `git status --short` solo muestra los archivos declarados en las tareas.
- T-006: `/api/agent/sdd` devuelve, en este orden y tras la política base, las reglas `shell` efectivas: `*` → `ask`, `git status *` → `allow`, `git diff *` → `allow`, `git log *` → `allow`, `git show *` → `allow`, `git rev-parse *` → `allow`, `git branch --show-current` → `allow`, `git branch --all *` → `allow`, `git add *` → `allow`, `git commit *` → `allow` y `python tools\sdd\validate.py *` → `allow`. La regla general `shell *` `ask` precede a toda la lista blanca y a la excepción del validador; `git push *` y `git tag *` conservan `ask` de la configuración global y cualquier otro comando resuelve a `ask`.
- T-006: `.opencode/agents/sdd.md` conserva CRLF en todas sus líneas (112 CR y 112 LF) y termina con salto de línea final (bytes `73 2E 0D 0A`), lo que cierra la observación O-02 sin cambios en el cuerpo del documento.
- T-006: `python tools\sdd\validate.py --all` devuelve `OK: sin hallazgos.` con código de salida 0.
- T-006: `git diff --check` sin hallazgos; el diff de `.opencode/agents/sdd.md` solo añade las diez reglas `shell` y el salto de línea final.
- T-007: contraste de la tabla «Etapa, subagente y precondición» con `docs\sdd\PROTOCOLO_OPERATIVO.md` §2 (G1 fin de Clarify, G2 fin de Tasks, G3 fin de Implement, G4 fin de Validate), fila por fila:
  - `3 Clarify` → precondición «rama `feat/*` creada y `spec.md` en `draft`»: la compuerta que produce Clarify es G1 (fin de Clarify), por lo que ni G1 ni G4 pueden exigirse para entrar; entrada habilitada por rama y `spec.md` en `draft`. Sin circularidad.
  - `4 Plan` → «G1 aprobada y spec en `clarified`»: G1 es fin de Clarify y `clarified` es el estado posterior a esa compuerta; coinciden.
  - `5 Tasks` → «spec en `planned`»: `planned` es el estado que sigue a Plan; la compuerta G2 se produce al final de Tasks, no antes.
  - `6 Implement` → «G2 aprobada y spec en `tasked`»: G2 es fin de Tasks y `tasked` el estado posterior; la precondición es correcta y ya no exige G4.
  - `7 Validate` → «G3 completa (todas las tareas `[x]`)»: G3 es fin de Implement; G4 se produce dentro de Validate, de modo que no puede ser precondición.
  - Resultado: las cinco filas son coherentes con §2 y no queda ninguna mención a G4 como precondición de Implement. `G4` solo persiste donde corresponde: la plantilla de Validate («contra la compuerta G4») y la regla 8 («G1, G4 y G6 son del propietario», coherente con PROTOCOLO §6).
- T-007: regla 2 de «Reglas de orquestación» queda «No lances `coder` sin G2 aprobada; no lances `reviewer` sin G3 completa», alineada con las compuertas de §2 y con CB-001.
- T-007: las plantillas de Implement y Validate incorporan ahora el literal «Etapa: implement» y «Etapa: validate», de modo que las seis solicitudes declaran spec, etapa y resultado esperado (RF-007).
- T-007: la línea de función previa a «Orquestación de subagentes» enumera `planner`, `coder`, `reviewer` y `explore`, coherente con las reglas `subagent` del frontmatter.
- T-007: `/api/agent/sdd` sirve el cuerpo actualizado (aparecen «G2 aprobada», «Etapa: implement», «Etapa: validate» y «`explore` cuando»), el frontmatter se conservó intacto, el archivo mantiene CRLF (112 CR y 112 LF) con salto de línea final, `python tools\sdd\validate.py --all` devuelve `OK: sin hallazgos.` con código 0 y `git diff --check` no reporta hallazgos.
- T-008: `/api/agent` mantiene `coder | mode=all` y `planner | mode=all`, y `/api/agent/planner` y `/api/agent/coder` devuelven ambos la regla `subagent | * | deny` como última regla declarada de su lista de permisos (índice 13 de 16 en `planner`; índice 14 de 17 en `coder`), por lo que la política base `* * allow` queda sobrescrita para cualquier subagente.
- T-008: `planner` conserva sus reglas `edit * deny` y `edit specs/** allow` previas; `coder` conserva `edit specs/** deny`, `edit docs/** deny` y `edit specs/*/tasks.md allow`. Ninguna regla `edit` se alteró y el cuerpo de ambos documentos quedó intacto.
- T-008: la restricción es coherente con `docs\sdd\PROTOCOLO_OPERATIVO.md` §10, que atribuye la capacidad de lanzar subagentes solo a `sdd` («Solo lectura; puede lanzar subagentes»).
- T-008: ambos archivos mantienen CRLF (39 CR y 39 LF cada uno) y salto de línea final (`planner.md` → `6F 2E 0D 0A`; `coder.md` → `61 2E 0D 0A`); `python tools\sdd\validate.py --all` devuelve `OK: sin hallazgos.` con código 0 y `git diff --check` no reporta hallazgos.
