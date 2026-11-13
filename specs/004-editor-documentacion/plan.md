# Plan técnico — SPEC-004

## Referencias

- `spec.md`: `SPEC-004`, versión 0.3.0, estado `clarified`, G1 aprobada el 2026-11-13.
- `clarify.md`: `SPEC-004`, cerrado con AMB-001 a AMB-004 resueltos y parches aplicados.

## Arquitectura de módulos

- **Definición del subagente `documenter`** (`.opencode/agents/documenter.md`, nuevo). Modo `subagent`. Permisos de mínimo privilegio (RF-002, RF-003, CB-002, CB-003). Cuerpo con las reglas de correcciones (RF-005), la parada ante cambios de requisitos o código (CB-001) y la conservación de CRLF (RNF-003).
- **Orquestador `sdd`** (`.opencode/agents/sdd.md`, modificado). Añade `documenter` a su lista blanca de subagentes (RF-001) y a la lista de subagentes de la sección de orquestación. Añade la fila de etapa y la forma de la solicitud (RF-004).
- **Documentación normativa** (modificada para RF-006):
  - `docs/sdd/PROTOCOLO_OPERATIVO.md`, §6 (compuerta G4).
  - `AGENTS.md`, línea de G4 en «Desarrollo (SDD)».
  - `docs/Flujo_de_Trabajo_Git.md`, bullet de commits autorizados de `dev` y procedimiento de release (excepción de contabilidad).
- **Registro de cambios** `CHANGELOG.md`, entradas bajo `Unreleased` (RNF-002).
- **Registro de specs** `specs/INDEX.md`, estado de SPEC-004.

Flujo de ejecución:

```text
sdd --(solicitud: Spec, Etapa, Resultado esperado)--> documenter
documenter --(edita solo docs/** y AGENTS.md)--> reporta o se detiene (CB-001)
sdd --(commit docs: con Spec: SPEC-004)--> dev
```

## Esquemas, tipos e interfaces

### Frontmatter de `.opencode/agents/documenter.md`

```yaml
---
description: Aplica correcciones editoriales y normativas en docs/ y AGENTS.md. Invocable por sdd como subagente. No toca código ni requisitos.
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: deny
  - action: subagent
    resource: "*"
    effect: deny
  - action: edit
    resource: "docs/**"
    effect: allow
  - action: edit
    resource: "AGENTS.md"
    effect: allow
---
```

El orden cumple RNF-001: todas las reglas generales (`resource: "*"`) de denegación de edición, de shell y de subagentes van antes que las excepciones de `docs/**` y `AGENTS.md`. La denegación de shell se coloca entre las generales y no al final, porque una regla general posterior a las excepciones incumpliría RNF-001. Su efecto sobre `shell` es el mismo en cualquier posición, porque no existe ninguna excepción de shell.

### Cambio en `.opencode/agents/sdd.md`

Se añade una regla tras la de `reviewer`, con el mismo formato que las existentes:

```yaml
  - action: subagent
    resource: documenter
    effect: allow
```

### Interfaz de solicitud a `documenter` (RF-004, AMB-004)

```text
Spec SPEC-004 en specs/004-editor-documentacion/. Etapa: <etapa en curso>.
Corrección: <documento y cambio exacto>.
Resultado esperado: <resultado verificable>.
```

### Texto normativo resultante (RF-006, AMB-003)

- `docs/sdd/PROTOCOLO_OPERATIVO.md` §6: «- **G4**: el propietario aprueba la implementación validada (validation_report.md al 100 %).»
- `AGENTS.md`, línea G4: «G4 (implementación validada)».
- `docs/Flujo_de_Trabajo_Git.md`:
  - En el bullet del commit `chore: prepare release vX.Y.Z`, sustituir «solo puede modificar `CHANGELOG.md`» por «puede modificar `CHANGELOG.md`, el índice de specs y el frontmatter de la spec de la release, con autorización del propietario».
  - En el procedimiento de release, añadir `specs/INDEX.md` y el frontmatter de la spec a los archivos del commit, junto a `CHANGELOG.md`.
  - Documentar la prioridad de versiones de AMB-003 (d).

## Decisiones técnicas

### DEC-001

- **Decisión:** `documenter` se define con una lista de permisos ordenada: primero las denegaciones generales de edición, de shell (AMB-006) y de subagentes, y después las excepciones de `docs/**` y `AGENTS.md`. Así se cumple RNF-001 y se deniegan por defecto `specs/`, `src/`, `tools/` y `.opencode/` (AMB-002). La denegación de shell impide que el agente escriba archivos mediante comandos, de modo que solo edita archivos.
- **Alternativas descartadas:**
  - Excepciones antes de la regla general: se descarta porque incumple RNF-001.
  - Edición permitida en general con lista de denegaciones: se descarta porque la lista sería incompleta frente a CB-002.

### DEC-002

- **Decisión:** `sdd` incorpora `documenter` a su lista blanca de subagentes con una regla específica. No se abre `subagent *`, para mantener el principio de mínimo privilegio de `sdd`.
- **Alternativas descartadas:**
  - Permitir `subagent *` en `sdd`: se descarta porque amplía la delegación más allá de RF-001.

### DEC-003

- **Decisión:** El cuerpo de `documenter` prohíbe cambiar requisitos, comportamiento o código, exige detenerse sin editar ante una corrección de ese tipo (CB-001) y reportar el motivo al orquestador. Los permisos no pueden expresar ese juicio, por eso se fija en el cuerpo del agente.
- **Alternativas descartadas:**
  - Confiar solo en los permisos: se descarta porque los permisos no distinguen una errata de un cambio de requisito dentro de `docs/`.

### DEC-004

- **Decisión:** Las correcciones normativas de O-02 se aplican con `documenter`, invocado por `sdd`, y se registran en un único commit `docs:` con `Spec: SPEC-004` en el cuerpo. `sdd` ejecuta el commit porque ya tiene permiso para `git add` y `git commit`. Un commit `docs:` describe mejor el cambio que `chore:`, y el flujo permite ambos tipos para cambios editoriales.
- **Alternativas descartadas:**
  - Commit `chore:`: válido, pero describe peor un cambio normativo.
  - Aplicar las correcciones a mano sin agente: se descarta porque rompe la trazabilidad que pide RF-006.

### DEC-005

- **Decisión:** La verificación de la configuración usa `opencode api get /api/agent` y `opencode api get /api/agent/sdd`, ejecutados desde la raíz del repositorio. Se comprueba que aparecen `documenter` con `mode: subagent`, el orden de permisos de DEC-001 y la regla de `documenter` en `sdd`. Si el endpoint no lista los agentes del repositorio, T-005 se registra como BLOQUEADA y no como aprobada.
- **Observación de la etapa de plan:** La consulta realizada en esta etapa devolvió solo los agentes internos (`build`, `general`, `explore`, `compaction`, `title`, `summary`, `plan`), tanto desde la raíz del repositorio como con `--standalone`. No aparecieron `sdd`, `planner`, `coder` ni `reviewer`. Por tanto, la verificación de DEC-005 no está comprobada todavía.
- **Alternativas descartadas:**
  - Verificar solo leyendo el texto de los archivos: se descarta porque no prueba la carga efectiva del agente.

### DEC-006

- **Decisión:** `coder` es el ejecutor de T-001 y T-002 por autorización del propietario (AMB-005, 2026-11-13). Es una excepción explícita a la descripción de §10 del protocolo, que asigna a `coder` solo `src/**`, `tests/**`, `tools/**` y `tasks.md`. La excepción se limita a `.opencode/agents/` y no modifica el protocolo en esta spec.
- **Alternativas descartadas:**
  - Modificar el protocolo §10 en esta spec: se descarta porque el propietario pidió no modificar el protocolo aquí.
  - Que el propietario edite manualmente T-001 y T-002: se descarta porque el propietario decidió autorizar a `coder`.
  - Dar a `documenter` escritura en `.opencode/`: se descarta por AMB-002 y CB-002.

## Estrategia de testing

- **Código Python:** no se escribe código de producción en esta spec. No aplica TDD.
- **Scripts `.bat`:** no aplican.
- **Configuración de agentes:** comprobación con `opencode api get` (DEC-005) y lectura del frontmatter con búsquedas por patrón.
- **Documentación:** búsquedas literales de los textos de AMB-003 en los tres documentos normativos y en la entrada de `CHANGELOG.md`.
- **Formato:** `git diff --check`, y comprobación de CRLF y salto final en cada archivo editado (RNF-003).
- **Validador:** `python tools\sdd\validate.py --spec SPEC-004 --gate G2` y `python tools\sdd\validate.py --all`.

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | `sdd` (regla de subagente) | T-002: `opencode api get /api/agent/sdd` muestra `documenter` permitido |
| RF-002 | `documenter` (permisos de edición y shell) | T-005: permisos efectivos de `documenter` en `docs/**` y `AGENTS.md`; `shell *` denegado (AMB-006) |
| RF-003 | `documenter` (permiso de subagentes) | T-005: permiso `subagent *` denegado |
| RF-004 | `sdd` (interfaz de solicitud) | T-002: búsqueda de «Etapa:» y «Resultado esperado» en `sdd.md` |
| RF-005 | `documenter` (cuerpo del agente) | T-001: búsqueda de la regla editorial y normativa; T-005: revisión del cuerpo |
| RF-006 | `PROTOCOLO_OPERATIVO.md`, `AGENTS.md`, `Flujo_de_Trabajo_Git.md` | T-003: búsqueda de los textos de AMB-003 |
| RNF-001 | `documenter` (orden de permisos) | T-001: orden verificado por lectura, con generales (edición, shell, subagentes) antes de excepciones; T-005: orden en la respuesta de la API |
| RNF-002 | `CHANGELOG.md` | T-004: entrada bajo `Unreleased` que menciona `SPEC-004` |
| RNF-003 | Archivos editados | T-003 y T-005: CRLF y salto final por archivo |
| CB-001 | `documenter` (cuerpo del agente) | T-001: regla de parada presente; T-003: no se modifican requisitos |
| CB-002 | `documenter` (permisos de edición) | T-005: edición de `specs/`, `src/`, `tools/` y `.opencode/` denegada en reglas efectivas |
| CB-003 | `documenter` (permiso de subagentes) | T-005: permiso de lanzamiento denegado en reglas efectivas |

## Restricciones de ejecución pendientes de decisión del propietario

Estas restricciones no cambian los requisitos. Afectan a quién puede ejecutar cada tarea y deben resolverse antes de G2:

1. **Resuelto: T-001 y T-002 escriben en `.opencode/`.** AMB-005 y DEC-006 autorizan a `coder` como ejecutor de estas dos tareas, como excepción a §10 del protocolo, que no se modifica en esta spec.
2. **T-004 escribe en `CHANGELOG.md`.** `documenter` no puede (CB-002), `planner` no puede y `coder` no tiene asignada esa escritura en el protocolo. Hace falta decidir quién ejecuta esta tarea.
3. **Estado `planned` omitido.** El protocolo (§2) define `draft → clarified → planned → tasked`. Por instrucción del propietario, el frontmatter pasa directamente de `clarified` a `tasked`, con versión 0.4.0. Hace falta confirmar esta excepción.
4. **Protocolo §10 sin `documenter`.** La tabla de agentes no incluye `documenter`. Actualizarla queda fuera de O-02 y requiere decisión.
5. **Resuelto para `documenter`: escritura por shell.** AMB-006 añade `shell *` denegado, de modo que `documenter` solo edita archivos. Los demás agentes conservan el mismo riesgo de shell, que queda fuera de esta spec.
