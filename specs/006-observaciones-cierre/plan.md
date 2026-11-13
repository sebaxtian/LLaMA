# Plan técnico - SPEC-006

## Referencias

- `spec.md`: `SPEC-006` (versión 0.3.0, estado `tasked`).
- `clarify.md`: `SPEC-006` (AMB-001 a AMB-003).
- `specs/005-compuertas-completas/clarify.md`: destino de la nota de confirmación (RF-003).
- `docs/sdd/PROTOCOLO_OPERATIVO.md` §10: tabla de agentes y permisos (RF-001).
- `MEMORY.md`: memoria operativa (RF-002).
- `CHANGELOG.md`: registro de cambios bajo Unreleased (RNF-002).
- `.opencode/agents/*.md`: permisos efectivos de cada agente, verificados con `opencode debug agents` desde la raíz del repositorio.

## Arquitectura de módulos

Esta spec solo modifica documentación. No cambia código, validador, `.opencode/` ni `opencode.jsonc`.

- **Protocolo operativo (§10):** una fila de tabla. Lo edita `documenter`, que tiene permiso sobre `docs/**`.
- **Memoria operativa:** una línea de la lista de `.opencode/` y una viñeta nueva sobre la consulta de agentes. Lo edita `coder`, que tiene permiso general fuera de `specs/**` y `docs/**`.
- **Clarificación de SPEC-005:** una nota final. La edita `planner`, que tiene permiso sobre `specs/**`.
- **Registro de cambios:** una entrada bajo Unreleased. La edita `coder`, por la misma razón que la memoria.
- **Registro de specs y artefactos de SPEC-006:** los escribe `planner`. `sdd` registra en Git los artefactos de control.

## Esquemas

Fila de `sdd` en la tabla de §10 (DEC-001):

| Agente | Rol | Permisos |
|---|---|---|
| `sdd` | Orquestador de solo lectura sobre artefactos y código; registro de cambios Git de artefactos de control | Puede lanzar subagentes y ejecutar `git add` y `git commit` de artefactos de control |

Línea de la memoria operativa (DEC-002), en la viñeta de `.opencode/`:

- `.opencode/`: agentes del proyecto (`sdd`, `planner`, `coder`, `reviewer`, `documenter`), comandos `sdd-*` y skills. `explore` es el subagente integrado de OpenCode y no se define en el proyecto.

Viñeta nueva de consulta de agentes (DEC-002):

- Agentes del proyecto: ejecutar `opencode debug agents` con el directorio de trabajo en la raíz del repositorio. Desde otro directorio el comando devuelve solo los agentes por defecto.

Nota de confirmación al final de la clarificación de SPEC-005 (DEC-003):

```
## Nota de confirmación (SPEC-006)

- **Confirmación de AMB-001:** el propietario confirma que solo cuenta como superada una celda PASADO, con paréntesis de observación opcional. NO PASADO, PENDIENTE, PARCIAL y las celdas compuestas con estado negativo son error.
- **Fecha:** 2026-11-13 (UTC).
- **Responsable:** Agent Sebaxtian.
```

## Decisiones técnicas

### DEC-001: fila de `sdd` en §10 con literal y límite

- **Decisión:** la fila usa el rol y los permisos definidos en AMB-001. El rol contiene el literal exigido por RF-005 de SPEC-005. Los permisos limitan el bookkeeping Git a `git add` y `git commit` de artefactos de control.
- **Alternativas descartadas:** (a) mantener la descripción actual y añadir una nota aparte: no cumple el literal en la tabla. (b) describir `sdd` como de solo lectura sin matiz: contradice la allowlist de `shell` que permite `git add` y `git commit`.

### DEC-002: memoria operativa con lista de agentes y consulta

- **Decisión:** la línea de `.opencode/` enumera los agentes del proyecto y la viñeta nueva documenta el comando `opencode debug agents` desde la raíz. `explore` se nombra como integrado. El parámetro `location[directory]` no se documenta, porque no se pudo verificar (AMB-002).
- **Alternativas descartadas:** (a) documentar `location[directory]` sin verificar: un dato no comprobado no debe entrar en la memoria operativa. (b) crear una sección nueva: añade un cambio mayor que el necesario para RF-002.

### DEC-003: nota de confirmación al final de la clarificación de SPEC-005

- **Decisión:** la nota se añade al final de la clarificación de SPEC-005, sin tocar su punto «a confirmar», sus decisiones ni sus parches. Así el historial queda intacto y se registra la confirmación.
- **Alternativas descartadas:** (a) editar el punto «a confirmar» de AMB-001: altera el texto ya aprobado y pierde el historial. (b) registrar la confirmación solo en esta spec: no cumpliría RF-003, que exige el registro en SPEC-005.

## Estrategia de testing

Esta spec no tiene pruebas automatizadas nuevas. La verificación es documental y se apoya en el validador y en comprobaciones de texto.

- **Validador:** `python tools\sdd\validate.py --spec SPEC-006 --gate G2` y `python tools\sdd\validate.py --all` deben devolver `0`. Las advertencias de artefactos aún no creados deben desaparecer al completar la etapa.
- **Regresión:** `python -m unittest discover -s tools\sdd\tests` debe ejecutar 47 pruebas con resultado `OK`. Ninguna prueba cambia.
- **Literal de §10:** búsqueda sin distinguir mayúsculas de «orquestador de solo lectura sobre artefactos y código» en la fila de `sdd`.
- **Memoria operativa:** búsqueda de los seis nombres de agente y del comando `opencode debug agents`.
- **Comando de consulta (CB-002):** ejecución de `opencode debug agents` desde la raíz (debe incluir los agentes del proyecto) y desde otro directorio (no debe incluirlos).
- **Nota en SPEC-005:** búsqueda de «Nota de confirmación (SPEC-006)» y de la fecha 2026-11-13.
- **Finales de línea (RNF-001):** comprobación de CRLF y salto final en cada archivo modificado.
- **Alcance (RNF-003):** `git diff --name-only` debe listar solo los archivos previstos en `tasks.md`.

## Matriz de cobertura

| Requisito | Componente | Prueba / comando |
|---|---|---|
| RF-001 | Protocolo §10 | Búsqueda del literal en la fila de `sdd` (T-001) |
| RF-002 | Memoria operativa | Búsqueda de los seis agentes y del comando; ejecución del comando desde la raíz (T-002) |
| RF-003 | Clarificación de SPEC-005 | Búsqueda de la nota y de su fecha y responsable (T-003) |
| RNF-001 | Archivos modificados | Comprobación de CRLF y salto final (T-005) |
| RNF-002 | Registro de cambios | Búsqueda de la entrada de SPEC-006 bajo Unreleased (T-004) |
| RNF-003 | Conjunto de cambios | `git diff --name-only` frente a la lista prevista (T-005) |
| CB-001 | Ejecutores | Si T-001 o T-002 requieren otros permisos, el ejecutor se detiene y reporta (T-001, T-005) |
| CB-002 | Memoria operativa | Ejecución del comando desde otro directorio (T-002, T-005) |
