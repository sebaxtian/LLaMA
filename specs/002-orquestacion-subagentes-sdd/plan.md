# Plan técnico - SPEC-002

## Referencias

- `spec.md`: `SPEC-002`.
- `clarify.md`: `SPEC-002`.
- `docs/sdd/PROTOCOLO_OPERATIVO.md` §10 (agentes y permisos) y §9 (validador determinista).
- `docs/sdd/guia_subagentes_opencode_sdd.md` §7 (modo `subagent` obligatorio para delegar).

## Arquitectura de módulos

La feature no introduce código ejecutable. Ajusta tres definiciones de agentes en `.opencode/agents/`:

1. `planner.md`: cambia `mode` de `primary` a `all`, explicita en `description` que es invocable por `sdd` y deniega `subagent`.
2. `coder.md`: mismo cambio de `mode` y de `description`, y la misma denegación de `subagent`.
3. `sdd.md`: añade reglas `subagent` explícitas, una regla general `shell *` con efecto `ask` más una lista blanca de solo lectura y del validador, y una sección operativa de orquestación.

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

### DEC-006

- **Decisión:** la compuerta G4 se solicita al final de Validate; la etapa Implement se gatea con G2 verificada con `python tools\sdd\validate.py --spec SPEC-002 --gate G2` y la spec en `tasked`. G2 no es una aprobación humana: §6 reserva la aprobación a G1, G4 y G6 (AMB-008).
- **Alternativas descartadas:** exigir G4 antes de Implement (lectura de PROTOCOLO §6) hacía la etapa inalcanzable porque G4 exige un `validation_report.md` convergido; gatear Implement con G1 dejaría sin control el paso de Tasks a Implement.
- **Motivo:** reconcilia `docs/sdd/PROTOCOLO_OPERATIVO.md` §2 (G3 fin de Implement, G4 fin de Validate) con la práctica del proyecto; §6 se interpreta como aprobación de la implementación ya realizada. Resuelve B-02 y B-03 (AMB-005).

### DEC-007

- **Decisión:** la acción `shell` se declara con la regla general `shell *` con efecto `ask`, seguida de `allow` para el validador (`python tools\sdd\validate.py *`) y para la lista blanca exacta: `git status *`, `git diff *`, `git log *`, `git show *`, `git rev-parse *`, `git branch --show-current`, `git branch --all *`, `git add *` y `git commit *`. Merge, tag y push permanecen en `ask`. `git add *` y `git commit *` son una excepción autorizada por el propietario el 2026-11-13 (UTC) a la descripción «Solo lectura» de `docs/sdd/PROTOCOLO_OPERATIVO.md` §10; el resto de la descripción se mantiene.
- **Alternativas descartadas:** `shell * deny` bloquea el validador que RNF-001 y RF-006 necesitan; dejar solo la excepción `allow` del validador, como en DEC-003, hereda la política base `allow` y no acota nada (B-01).
- **Motivo:** el orden «general antes de excepciones» de RNF-001 produce una lista blanca efectiva con confirmación humana fuera de ella. Sustituye a DEC-003 en el acotamiento de `shell` (AMB-006).

### DEC-008

- **Decisión:** declarar `{ action: subagent, resource: "*", effect: deny }` en `planner.md` y en `coder.md`.
- **Alternativas descartadas:** confiar en la política base, que les concede `subagent * allow` por herencia y les permite delegar en `general` o `explore`.
- **Motivo:** el protocolo §10 reserva el lanzamiento de subagentes a `sdd`; la denegación explícita satisface RNF-001 y el mínimo privilegio (AMB-007, B-04).

## Estrategia de testing

- Validación determinista: `python tools\sdd\validate.py --all`, `--spec SPEC-002 --gate G2` y `--spec SPEC-002 --gate G4`.
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
| CB-001 | sección de orquestación | regla explícita de G2 previa a Implement |
| CB-002 | sección de orquestación | regla de bloqueo registrado |
| CB-003 | sección de orquestación | regla de parada por error del validador |
| CA-007 | `sdd.md` regla 1 | contraste del código de salida del validador y parada ante valor distinto de `0` |
| CA-008 | `sdd.md` §«Solicitudes» y regla 6 | revisión de la plantilla y del bloqueo registrado |
| CA-009 | `permissions` de `sdd.md`, `planner.md` y `coder.md` | `/api/agent` muestra las reglas generales antes de las excepciones |
| CA-010 | `CHANGELOG.md` | entrada bajo `Unreleased` antes de la release |
| T-006 | `sdd.md` regla general `shell *` y lista blanca | `/api/agent/sdd` muestra la regla general antes de las excepciones |
| T-007 | `sdd.md` tabla de precondiciones y regla 2 | contraste con PROTOCOLO §2 sin contradicción |
| T-008 | `planner.md` y `coder.md` `subagent * deny` | `/api/agent` muestra la denegación en ambos |
| RF-006, CB-003 | `sdd.md` fila 6 y regla 1 (T-009) | `/api/agent/sdd` y contraste con el código de salida del validador |
| RNF-002 | `CHANGELOG.md` `Unreleased` (T-010) | entrada que refleja la configuración final |

## Alcance de la reapertura

La corrección del validador determinista queda fuera de esta spec: `validate.py` acepta la subcadena `CONVERGIDO` y por tanto admite un dictamen `NO CONVERGIDO` como convergencia (observación O-01 de `validation_report.md`), y su chequeo de cobertura no verifica `RF/CB → CA` (B-05). Endurecer esas dos comprobaciones requiere spec propia; aquí solo se corrigen los artefactos y la configuración de agentes.