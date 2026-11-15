# Plan final de cierre de brechas del flujo SDD

**Proyecto:** LLaMA  
**Fecha:** 2026-11-14  
**Estado:** planificación; no ejecutado  
**Base:** auditoría de `@reviewer` sobre norma/validador y revisión de `@explore` sobre Git, OpenCode y el árbol real.

> Este archivo es un plan. No aprueba G1, G4 ni G6, no crea una spec y no autoriza cambios en el repositorio.

---

## 1. Objetivo y límites

### Objetivo

Hacer que el flujo SDD sea auditable de extremo a extremo: que las compuertas no se presenten como superadas sin la evidencia normativa, que los permisos de agentes no permitan alterar arbitrariamente el objeto auditado y que la documentación describa el estado real del proyecto.

### Límites del plan

- No se modifica `llama.cpp/`, modelos, binarios, `.env` ni artefactos locales.
- `feat/gemma-4-26b-a4b-it-qat-gguf` se deja intacta y no se usa como base.
- No se ejecutan pruebas remotas contra GitHub durante la validación normal.
- No se cierra en esta iteración la cadena `CA → T`, la evidencia por tarea, las transiciones históricas completas ni el alcance del diff.
- CI, hooks y protección de secretos quedan como decisión posterior; no se introducen de forma implícita.

---

## 2. Decisiones adoptadas y decisiones pendientes

### 2.1 Decisiones adoptadas

| ID | Decisión |
|---|---|
| D-001 | Se trabajará en dos specs secuenciales: SPEC-008 de gobernanza y SPEC-009 del validador. |
| D-002 | La rama `feat/gemma-4-26b-a4b-it-qat-gguf` no se borra, etiqueta, integra ni usa como base. |
| D-003 | Los permisos efectivos se verifican y endurecen antes de delegar implementación a un subagente. |
| D-004 | El trabajo documental pendiente se separa primero en una rama `docs/*`; no se mezcla con SPEC-008. |
| D-005 | La suite normal de validación solo ejecuta `tools/sdd/tests`; los tests que mutan GitHub serán opt-in y no forman parte del gate normal. |

### 2.2 Decisiones que deben cerrarse en Clarify

| ID | Decisión requerida | Recomendación |
|---|---|---|
| D-006 | Quién escribe `implementing`, `implemented` y `validated` | El propietario, mediante un procedimiento explícito; los agentes solo preparan la evidencia. |
| D-007 | Cómo se demuestra G5 retrospectivamente | Artefacto de evidencia de integración o contrato Git inequívoco; no inferencia heurística. |
| D-008 | Cómo se demuestra G6 | Tag anotado + `CHANGELOG.md` + `INDEX.md` + aprobación; conservar evidencia antes de que se borre la rama. |
| D-009 | Valor de `default_agent` | Mantener `plan` como arranque seguro en solo lectura y documentar que no equivale a `planner`. |
| D-010 | CI | No incluirlo en SPEC-008/009; abrir una spec separada si se quiere automatizar el gate. |

Si D-006 o D-007 no tienen una solución verificable, el requisito correspondiente se reduce a documentación y checklist, no se implementa de forma especulativa.

---

## 3. Diagnóstico de partida

### 3.1 Estado del repositorio

| Comprobación | Resultado verificado |
|---|---|
| `dev` y `main` frente a remoto | Sin divergencia (`0/0`). |
| Tags | 8 anotados con asunto `Release vX.Y.Z`. |
| Merges en `dev` | 26, con dos padres. |
| Specs | SPEC-001 a SPEC-007, todas `released`. |
| `validate.py --all` | Código 0, sin hallazgos. |
| Tests SDD | 47 métodos en verde. |
| Siguiente ID | `SPEC-008`. |
| Worktree | Modificados `docs/sdd/diagrama_flujo_ciclo_vida_sdd.md` y `docs/sdd/guia_maestra_sdd.md`. |
| CI/hooks | No hay workflow ni hook activo. |
| Rama Gemma | 2 commits, 47 detrás de `dev`, diff de −13 680 líneas; sin spec. |
| Referencia remota | `origin/release/v0-6-0` es obsoleta; no existe en `ls-remote`. |

### 3.2 Brechas confirmadas relevantes

1. Las aprobaciones G1/G4/G6 no se verifican.
2. G5 y G6 carecen de lógica propia.
3. La ausencia de artefactos es WARN sin depender correctamente del estado.
4. Las transiciones de estado no se validan.
5. Ningún comando posee de forma clara la escritura de estados 6–7.
6. La cobertura `RF/CB → CA` no bloquea las compuertas.
7. La relación `CA → T` no se verifica.
8. Un reporte sin matriz puede pasar G4.
9. `--git` no verifica alcance del diff y se ignora con `--all`.
10. `supersedes` y `superseded_by` no se validan semánticamente.
11. `--all` no comprueba tareas abiertas en estados finales.
12. `INDEX.md` solo se contrasta por existencia de `spec.md`.
13. `/sdd-implement` exige G4 donde corresponde G2 y valida G3 por tarea.
14. La plantilla de `spec.md` no incluye G4.
15. La afirmación «19 documentos frente a 21» es falsa como brecha: 21 `.md` equivalen a README + protocolo + 19 referencias. El defecto real es que `guia_maestra_sdd.md` no está indexada en `docs/sdd/README.md`.

### 3.3 Brechas adicionales de gobierno

- Los permisos de `edit` se pueden eludir mediante `shell` en varios agentes.
- `reviewer` no tiene un aislamiento efectivo frente a shell/subagentes.
- `coder` puede alcanzar archivos fuera de su rol mediante shell.
- Los globs globales `*` pueden no proteger rutas anidadas; debe verificarse la semántica real antes de cambiar a `**`.
- La rama Gemma elimina infraestructura al compararla con `dev`; queda expresamente fuera.
- `tools/git/tests` contiene pruebas con efectos remotos; no se ejecuta como suite general.
- `README.md` y `MEMORY.md` contienen afirmaciones históricas desactualizadas.

---

## 4. Fase −1: saneamiento documental y aislamiento

**Tipo:** `docs:`/higiene local.  
**Rama:** `docs/cierre-documental-sdd`.  
**No incluye:** cambios en `validate.py`, permisos de agentes ni tests remotos.

### T−1.1 — Aislar el trabajo documental existente

Crear la rama desde el estado actual de `dev` sin incorporar `feat/gemma`. Confirmar que los dos documentos modificados pertenecen al alcance del PR y que no hay archivos sin seguimiento.

### T−1.2 — Corregir el documento del diagrama

En `docs/sdd/diagrama_flujo_ciclo_vida_sdd.md`, sustituir la fila de la supuesta brecha 15 por:

> `guia_maestra_sdd.md` no está indexado en `docs/sdd/README.md` | Documento de referencia no incluido en el orden de lectura.

No afirmar que el protocolo cuenta mal los documentos.

### T−1.3 — Indexar la guía maestra

Añadir `guia_maestra_sdd.md` a `docs/sdd/README.md` como documento de referencia no normativo.

### T−1.4 — Actualizar documentación operativa

Corregir únicamente hechos comprobados:

- `README.md`: `main.bat` existe; añadir `documenter`; corregir la descripción de `docs/` y eliminar el pendiente histórico del menú.
- `MEMORY.md`: indicar que hay 3 `.gguf` locales bajo `models/`, que `main.bat` está implementado y que la rama Gemma no es una base integrable.

No alterar reglas normativas en esta tarea.

### T−1.5 — Registrar el trabajo documental

Añadir a `CHANGELOG.md` bajo `Unreleased` solo los cambios realmente incluidos en el PR: diagrama canónico, eliminación de duplicación, índice y actualización de contexto operativo.

### T−1.6 — Higiene local segura

Ejecutar `git remote prune origin` solo para eliminar la referencia local obsoleta `origin/release/v0-6-0`. No borrar ramas remotas ni modificar GitHub.

### Criterios de salida de la Fase −1

- `git diff --check` limpio.
- `python tools\sdd\validate.py --all` devuelve 0.
- El PR contiene solo documentación y la higiene local permitida.
- El PR se integra con `merge --no-ff` antes de iniciar SPEC-008.
- No se modifica `tools/git/tests` en esta fase.

---

## 5. SPEC-008: gobernanza, comandos y permisos

**Nombre propuesto:** `008-gobernanza-permisos-transiciones`.  
**Rama:** `feat/gobernanza-permisos`, creada desde `dev` después de integrar Fase −1.  
**Base:** plantilla SDD vigente, con G4 añadido durante la propia spec si procede.

### 5.1 Propósito

Cerrar primero los defectos que pueden invalidar cualquier auditoría posterior: permisos efectivos, comando de implementación, ubicación de aprobaciones, dueño de estados y documentación operativa contradictoria.

### 5.2 Requisitos propuestos

**RF-008-001** — Cuando se configure un agente del proyecto, la política deberá denegar por defecto las operaciones de shell que escriban archivos fuera de su alcance y deberá conservar una allowlist explícita de comandos de lectura y validación.

**RF-008-002** — Cuando se configuren los guardrails globales, las rutas protegidas deberán cubrir recursivamente `llama.cpp/**`, `bin/**`, `models/**` y `.env`; la sintaxis deberá validarse con una prueba no destructiva de permisos efectivos.

**RF-008-003** — El agente `reviewer` no deberá poder lanzar subagentes ni modificar código/configuración durante una auditoría.

**RF-008-004** — El agente `coder` solo deberá editar los archivos de implementación y `tasks.md` declarados por la matriz de permisos; la shell no podrá ampliar ese alcance.

**RF-008-005** — El comando `/sdd-implement` deberá exigir G2 al iniciar implementación de una spec `tasked`, no G4.

**RF-008-006** — La validación de una tarea individual no deberá invocar G3 como si la etapa de implementación estuviera cerrada; G3 se reservará para el cierre de la etapa.

**RF-008-007** — El protocolo deberá declarar que la aprobación humana no puede ser escrita por un agente como sustituto del propietario, y deberá definir el procedimiento de registro de G1, G4 y G6.

**RF-008-008** — El protocolo deberá asignar un responsable explícito para cada cambio de `status`; si el responsable es el propietario, los comandos deberán imprimir la transición requerida sin escribirla automáticamente.

**RF-008-009** — El protocolo y las plantillas deberán fijar `spec.md` como registro canónico de G1/G4 y declarar informativa cualquier casilla equivalente del reporte.

**RF-008-010** — El procedimiento Git deberá documentar `delete_branch_on_merge: true` y que la evidencia necesaria para G5 se captura antes del merge que elimina la rama.

**RF-008-011** — La documentación de pruebas deberá distinguir la suite segura `tools/sdd/tests` de las pruebas remotas opt-in de `tools/git/tests`.

**RF-008-012** — El valor `default_agent: "plan"` deberá documentarse como arranque integrado de solo lectura y no como el agente `planner` del proyecto.

### 5.3 Tareas

| ID | Tarea | Responsable | Evidencia |
|---|---|---|---|
| T-008-001 | Probar la semántica real de permisos, globs y precedencia entre configuración global y agente | Propietario | Pruebas no destructivas y resultado registrado |
| T-008-002 | Aplicar deny/allowlist efectiva a `coder`, `reviewer`, `planner` y `sdd` | Propietario | Intentos fuera de alcance rechazados |
| T-008-003 | Proteger rutas recursivas y `.env` también frente a shell | Propietario | Pruebas de lectura/escritura rechazadas |
| T-008-004 | Corregir `/sdd-implement` de G4 a G2 y separar validación individual de G3 | Propietario o agente autorizado | Test textual de regresión |
| T-008-005 | Corregir protocolo, plantilla y procedimiento Git | Propietario/documenter autorizado | Diff documental revisado |
| T-008-006 | Definir propietario de los estados; no automatizar escritura si no hay permiso verificable | Propietario | Regla y procedimiento reproducible |
| T-008-007 | Añadir tests locales de configuración y comando, sin tests remotos | Coder después de T-008-002 | Suite SDD en verde |
| T-008-008 | Registrar la decisión sobre `default_agent` | Propietario | Referencia en documentación |

### 5.4 Restricción de permisos

Ningún subagente recibe tareas de implementación antes de completar T-008-001, T-008-002 y T-008-003. Si OpenCode no permite expresar una allowlist segura para shell, se documenta la limitación y se mantiene la implementación bajo ejecución del propietario; no se declara cerrado RF-008-001 por una configuración meramente textual.

### 5.5 Limitación sobre aprobaciones

Los permisos no prueban criptográficamente quién escribió `- Approved by: Agent Sebaxtian`. El cierre de esta parte requiere proceso de propietario, revisión independiente y, si se necesita no repudio, aprobación de PR o mecanismo de firma. La spec no debe prometer una garantía técnica que el formato Markdown no puede ofrecer.

### 5.6 Compuertas

G1 de SPEC-008 → T-008-001 a T-008-003 por el propietario → resto de tareas → G2/G3/G4 → PR a `dev`. G4 requiere aprobación humana; ningún agente la concede.

---

## 6. SPEC-009: validador de compuertas reales

**Nombre propuesto:** `009-validador-compuertas-reales`.  
**Rama:** `feat/validador-compuertas-reales`, creada desde `dev` después de integrar SPEC-008.  
**Prerequisito:** el contrato de evidencia de G5/G6 debe estar aprobado en Clarify.

### 6.1 Requisitos de bajo riesgo

**RF-009-001** — Cuando se valide G1 o G4, el validador deberá exigir en `spec.md` una aprobación marcada para la compuerta correspondiente, tolerando el formato real existente y fecha ISO.

**RF-009-002** — Cuando se valide G6, el validador deberá comprobar la aprobación en la sección de release de `CHANGELOG.md`, no en una casilla G6 inexistente de `spec.md`.

**RF-009-003** — Cuando se valide G4 o superior y se requiera `validation_report.md`, deberá existir al menos una matriz de trazabilidad reconocible con cabecera de requisito/criterio/CA y columna `Estado` o `Resultado`.

**RF-009-004** — Cuando el `status` implique un artefacto obligatorio, la ausencia del artefacto deberá ser ERROR; en estados previos solo podrá ser WARN.

**RF-009-005** — Cuando se ejecute `--all`, una spec en estado `implemented`, `validated` o `released` no podrá conservar tareas abiertas.

**RF-009-006** — El validador deberá comparar bidireccionalmente `INDEX.md` y frontmatter en ID, título, estado, rama, release y ruta.

**RF-009-007** — Con G2 o superior, la cobertura `RF/CB → CA` incompleta deberá ser ERROR; fuera de una compuerta podrá seguir siendo WARN.

**RF-009-008** — Los campos `supersedes` y `superseded_by` deberán validarse según el estado de sustitución y la existencia del destino.

### 6.2 G5/G6: diseño antes de implementación

No se implementará una heurística que busque cualquier merge de dos padres y lo atribuya a una spec. Antes de TDD se debe fijar:

- qué commit identifica la integración de la spec;
- cómo se relacionan merge, rama, release y tag;
- qué evidencia se conserva cuando `delete_branch_on_merge: true` elimina la rama;
- qué parte se valida localmente y qué parte requiere remoto;
- qué salida debe producir el validador cuando la evidencia histórica no existe.

Si el contrato no puede ser determinista con los datos actuales, G5/G6 se implementan como checklist/documentación y se abre una spec posterior para automatización.

### 6.3 Tareas TDD propuestas

| ID | Tarea | Evidencia |
|---|---|---|
| T-009-001 | Extraer despacho explícito por compuerta, sin umbrales implícitos | Tests de regresión del despacho |
| T-009-002 | Propagar `status` a validadores de artefactos | Fixtures por estado |
| T-009-003 | Validar aprobaciones G1/G4 con formatos reales | Fixtures de SPEC-002 y SPEC-007 |
| T-009-004 | Validar aprobación G6 en `CHANGELOG.md` | Fixture de release |
| T-009-005 | Exigir matriz de trazabilidad | Fixture sin matriz y tabla no reconocida |
| T-009-006 | Exigir artefactos por estado | Fixtures `planned`, `tasked`, `released` |
| T-009-007 | Exigir tareas cerradas por estado | Fixture con tarea abierta |
| T-009-008 | Validar `INDEX.md` en ambos sentidos | Fila huérfana, carpeta huérfana, campo divergente |
| T-009-009 | Elevar cobertura RF/CB a ERROR desde G2 | Fixture con cobertura ausente |
| T-009-010 | Validar sustitución | Destino inexistente y estado inválido |
| T-009-011 | Diseñar y, solo si es determinista, implementar G5 | Fixtures o Git simulado |
| T-009-012 | Diseñar y, solo si es determinista, implementar G6 | Tags y changelog simulados |
| T-009-013 | Actualizar documentación y decisiones supersedidas | Referencia a SPEC-005 y protocolo |

### 6.4 Fuera de SPEC-009

| Tema | Motivo |
|---|---|
| `CA → T` | Rompería 6 de 7 specs publicadas; requiere normalización separada. |
| Evidencia por tarea | Rompería 4 de 7 specs publicadas; requiere retrofitting explícito. |
| Historial completo de transiciones | Requiere resolver reaperturas, versiones y fuente de estado previo. |
| Alcance del diff | Requiere contrato de archivos permitidos y dos formatos documentales. |
| IDs duplicados | Mejora de calidad, no requisito mínimo de compuertas. |
| CI y hooks | Requieren decisión de infraestructura y una spec separada. |

### 6.5 Compuertas

G1 → G2 → implementación TDD → G3 → revisión independiente → G4 → PR a `dev`. G5 y G6 solo se declaran cerradas si existe el contrato de evidencia aprobado en Clarify.

---

## 7. Validación segura

### Gate normal

Ejecutar únicamente:

```bat
python tools\sdd\validate.py --all
python -m unittest discover -s tools\sdd\tests -q
python tools\sdd\validate.py --next-id
git diff --check
git status --short
```

No ejecutar `python -m unittest discover -s tools` como gate: incluye pruebas de `tools/git` con efectos remotos.

### Tests remotos

Los tests de `tools/git/tests` solo se habilitan con una variable explícita, revisión humana y un repositorio de prueba autorizado. La protección opt-in de esos tests no se incorpora en la Fase −1; si se desea, se especifica como tarea de gobernanza o como spec separada.

### Criterios de no regresión

1. Las 7 specs existentes siguen pasando `--all`.
2. Los 47 tests SDD existentes siguen en verde junto con los nuevos.
3. Las fixtures negativas fallan con código 1 y las positivas con código 0.
4. La validación estructural sin `--gate` no exige aprobación humana.
5. G1/G4/G6 no se consideran aprobadas solo por una mención textual fuera de su ubicación canónica.
6. No se ejecutan comandos de push, tag, branch protection o borrado remoto como parte del gate normal.

---

## 8. Release y evidencia

1. Integrar SPEC-008 en `dev` con `merge --no-ff`.
2. Integrar SPEC-009 en `dev` con `merge --no-ff`.
3. Ejecutar validación completa en `dev` y conservar sus salidas como evidencia.
4. Crear `release/v0-7-0` desde `dev` solo cuando el propietario autorice el release.
5. Capturar evidencia de G5 antes del merge, porque `delete_branch_on_merge: true` elimina la rama.
6. Actualizar `CHANGELOG.md`, `INDEX.md` y frontmatter según el procedimiento aprobado.
7. Integrar a `main` con `merge --no-ff`.
8. Crear tag anotado `v0.7.0` con asunto `Release v0.7.0` solo después de G6.

No se debe afirmar que G5/G6 están automatizadas si el contrato histórico no permite una comprobación determinista.

---

## 9. Matriz de trazabilidad mínima

| Requisito | Criterio | Tarea | Evidencia |
|---|---|---|---|
| RF-008-001 | CA-008-001 | T-008-001, T-008-002 | Permiso fuera de alcance rechazado |
| RF-008-005 | CA-008-005 | T-008-004 | Test textual G2, no G4 |
| RF-008-007 | CA-008-007 | T-008-005, T-008-006 | Procedimiento de aprobación humana |
| RF-009-001 | CA-009-001 | T-009-003 | Fixture sin aprobación falla G1/G4 |
| RF-009-003 | CA-009-003 | T-009-005 | Reporte sin matriz falla G4 |
| RF-009-004 | CA-009-004 | T-009-006 | Estado con artefacto faltante falla |
| RF-009-006 | CA-009-006 | T-009-008 | Índice divergente falla |
| RF-009-011 | CA-009-011 | T-009-011 | Solo si existe contrato G5 determinista |

---

## 10. Riesgos, limitaciones y mitigaciones

| Riesgo o limitación | Impacto | Mitigación |
|---|---|---|
| Los permisos de OpenCode pueden no soportar la allowlist esperada | Crítico | T-008-001 como prueba de viabilidad; no declarar cierre por configuración textual. |
| Shell puede eludir permisos de edición | Crítico | Deny efectivo o ejecución por propietario; pruebas negativas. |
| Markdown no demuestra autoría de una aprobación | Crítico | Aprobación humana por proceso/PR; documentar límite técnico. |
| G5 no puede inferirse de cualquier merge | Alto | Contrato de evidencia antes de codificar. |
| `--all` verde oculta deuda no modelada | Alto | Fixtures negativas y criterios específicos de compuerta. |
| `feat/gemma` sigue siendo destructiva | Crítico | No tocarla; todas las ramas nacen de `dev`; advertencia operativa. |
| `origin/release/v0-6-0` puede reaparecer por fetch | Medio | Podar localmente y no usar ramas remotas obsoletas como evidencia. |
| Tests de Git mutan GitHub | Alto | Gate SDD aislado; tests remotos opt-in y autorizados. |
| Falta de CI | Medio | Checklist manual; CI queda para spec posterior. |
| Ampliar documenter rompe mínimo privilegio | Alto | Mantener documenter en `docs/**`/`AGENTS.md`; propietario actualiza CHANGELOG/MEMORY/INDEX salvo spec de permisos explícita. |
| SPEC-005 contiene una decisión incompatible | Medio | Registrar supersesión en SPEC-009 antes de cambiar comportamiento de G3. |

---

## 11. Criterios finales de cierre

El plan solo se considera convergido cuando:

- Fase −1 está integrada y la documentación ya no contiene la brecha 15 refutada.
- SPEC-008 tiene G1, G4 y evidencia de que los permisos efectivos fueron probados antes de delegar.
- `/sdd-implement` coincide con G2/G3 del protocolo.
- El propietario de las transiciones y el procedimiento de aprobación están documentados.
- SPEC-009 tiene tests negativos para aprobaciones, matriz, artefactos, tareas e índice.
- G5/G6 solo se declaran automatizadas si su contrato determinista fue aprobado; en caso contrario quedan como checklist explícito.
- `validate.py --all`, la suite SDD segura, `git diff --check` y `git status --short` cumplen sus criterios.
- Ningún cambio no especificado se incorpora al PR.

---

## 12. Orden de ejecución

1. Revisar y aprobar este plan.
2. Ejecutar Fase −1 en rama documental y PR.
3. Crear SPEC-008 desde `dev` limpio; completar Specify, Clarify y G1.
4. El propietario ejecuta T-008-001 a T-008-003; solo después se delega el resto.
5. Completar SPEC-008 con TDD, G3, revisión y G4; integrar en `dev`.
6. Crear SPEC-009 desde `dev`; cerrar el contrato de G5/G6 en Clarify.
7. Implementar únicamente los checks deterministas; mantener fuera de alcance lo que requiera inferencia o retrofitting no aprobado.
8. Validar SPEC-009 y obtener G4; integrar en `dev`.
9. Preparar release `v0.7.0`, capturar G5 antes del merge y obtener G6 antes del tag.

## 13. Gobierno

Ninguna compuerta se aprueba dentro de este plan. G1, G4 y G6 corresponden al propietario. La línea `- Approved by: Agent Sebaxtian (YYYY-MM-DD)` es evidencia documental de aprobación, no una prueba criptográfica de autoría; el proceso de revisión humana debe cubrir esa limitación.
