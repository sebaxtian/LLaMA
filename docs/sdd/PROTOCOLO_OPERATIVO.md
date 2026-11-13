# Protocolo Operativo SDD del proyecto LLaMA

Este documento es la **norma ejecutable** del Desarrollo Basado en Especificaciones (SDD) del proyecto. Es de rango 3 en la jerarquía normativa: prevalece sobre el flujo Git y sobre los documentos de referencia de `docs/sdd/`, y cede ante `docs/constitution.md` y `AGENTS.md`.

El corpus de `docs/sdd/` (19 documentos) es material de referencia, no normativo. Ante contradicción con este protocolo, manda este protocolo.

## 1. Modelo de adopción

El proyecto adopta **SDD Spec-Anchored**: la especificación es el contrato vigente y convive con el código, validándose mutuamente. No se adopta Spec-as-Source (generación automática desde spec) ni Spec-First (spec descartable tras implementar).

## 2. Ciclo de vida: 7 etapas

| Etapa | Actividad | Artefacto | Estado resultante |
|---|---|---|---|
| 1 | Constitución / Setup | `constitution.md`, `AGENTS.md`, agentes, skills | — |
| 2 | Specify | `spec.md` | `draft` |
| 3 | Clarify | `clarify.md` + parches a `spec.md` | `clarified` |
| 4 | Plan | `plan.md` | `planned` |
| 5 | Tasks | `tasks.md` | `tasked` |
| 6 | Implement (TDD) | código + tests | `implementing` → `implemented` |
| 7 | Validate | `validation_report.md` | `validated` |

### Estados completos

```text
draft → clarified → planned → tasked → implementing → implemented → validated → released
  │         │           │          │
  └─────────┴───────────┴──────────┴──→ cancelled
validated → implementing (reapertura con motivo y nueva versión)
released / validated → superseded (sustitución explícita)
```

Las transiciones son solo hacia adelante. Una reapertura exige motivo registrado, incremento de versión y revalidación completa.

### Compuertas

| Compuerta | Momento | Condición |
|---|---|---|
| G1 | Fin de Clarify | `spec.md` sin ambigüedades, EARS correcto, aprobación del propietario |
| G2 | Fin de Tasks | `plan.md` y `tasks.md` conformes a la constitución y con cobertura 100 % |
| G3 | Fin de Implement | Todas las tareas `[x]` con evidencia; TDD en verde |
| G4 | Fin de Validate | `validation_report.md` converge al 100 %; aprobación de implementación |
| G5 | Integración Git | `merge --no-ff`, validación posterior, rama eliminada |
| G6 | Release | Autorización del propietario, tag anotado, `INDEX.md` y `CHANGELOG.md` actualizados |

## 3. Gramática de identificadores

Todos los IDs usan 3 dígitos y son únicos dentro de su espacio:

```text
SPEC-001   Especificación global (nunca reutilizada)
RF-001     Requisito funcional (notación EARS)
RNF-001    Requisito no funcional
CB-001     Caso borde
AMB-001    Ambigüedad / hallazgo de clarificación
CA-001     Criterio de aceptación
T-001      Tarea atómica
DEC-001    Decisión técnica
```

Referencia completa: `SPEC-001/RF-001`. Cadena obligatoria de trazabilidad:

```text
RF/CB → CA → T → evidencia → commit → merge → release
```

Ningún requisito sin criterio de aceptación, ningún criterio sin tarea, ninguna tarea sin validación declarada.

## 4. Contratos de artefactos

### `spec.md`

- Frontmatter: `id`, `title`, `status`, `version`, `created`, `updated`, `owner`, `branch`, `release`, `supersedes`, `superseded_by`.
- Secciones: contexto y objetivo, actores y permisos, requisitos EARS (`RF`), requisitos no funcionales (`RNF`), casos borde (`CB`), fuera de alcance, criterios de aceptación (`CA`), aprobaciones, historial de cambios.
- Prohibido incluir rutas de código, clases, frameworks, SQL o comandos técnicos. Eso pertenece a `plan.md`.
- Los `RF` usan notación **EARS** y contienen una palabra normativa (`DEBE`, `NO DEBE`, `DEBERÍA`, `PUEDE`).

### `clarify.md`

- Hallazgos `AMB-001` con pregunta, respuesta, fecha UTC y responsable.
- Casos borde nuevos (`CB-001`) y decisiones de negocio documentadas.
- Lista de parches aplicados a `spec.md`.
- No se autoriza `plan.md` hasta que `clarify.md` esté cerrado y los parches estén aplicados.

### `plan.md`

- Referencias a `spec.md` y `clarify.md`.
- Arquitectura de módulos, esquemas/tipos, interfaces, decisiones `DEC-001`.
- Estrategia de testing y matriz de cobertura `RF/CB → componente → prueba`.

### `tasks.md`

- Tareas `T-001` atómicas con: dependencias, requisitos cubiertos, archivos, estimación 15–30 min, comando de validación, checkboxes.
- Una tarea no puede tocar archivos fuera de su campo `Archivos`.

### `validation_report.md`

- Entorno, matriz `RF/CB → CA → prueba/comando → evidencia → estado`, brechas y dictamen `CONVERGIDO` solo al 100 %.

## 5. Notación EARS

Patrones obligatorios para `RF`:

| Tipo | Patrón |
|---|---|
| Ubiquitous | `El sistema DEBE <respuesta>`. |
| Event-driven | `CUANDO <evento>, el sistema DEBE <respuesta>`. |
| State-driven | `MIENTRAS <estado>, el sistema DEBE <respuesta>`. |
| Unwanted | `SI <condición>, ENTONCES el sistema DEBE <respuesta>`. |
| Optional | `DONDE <característica>, el sistema DEBE <respuesta>`. |

Todo umbral debe tener número y unidad. Léxico ambiguo prohibido en `RF`/`RNF`/`CA`: `TBD`, `TODO`, `por definir`, `etc.`, `y/o`, `apropiado`, `adecuado`, `óptimo`, `según sea necesario`, `cuando sea posible`.

## 6. Aprobaciones

- **G1**: el propietario aprueba `spec.md` y `clarify.md`.
- **G4**: el propietario aprueba la implementación validada (`validation_report.md` al 100 %).
- **G6**: el propietario autoriza el release.
- Línea de registro: `- Approved by: Agent Sebaxtian`.
- Prohibida la autoaprobación por parte de agentes.

## 7. Implementación

- **Python**: TDD estricto (Red → Green → Refactor). No se escribe código de producción sin un test que falle.
- **Scripts `.bat`**: validación-first (comando, salida esperada, código de salida y métricas declaradas antes de implementar).
- `/sdd-implement` ejecuta **una tarea pendiente por invocación**, salvo instrucción explícita del propietario.
- Si una tarea exige un archivo no declarado, se detiene y se actualiza `tasks.md` antes de continuar.
- Si aparece una ambigüedad no registrada, se detiene la implementación y se crea una `CLR`.
- No se modifican `RF`/`RNF`/`CA` para que encajen con el código; un cambio de requisito tras `clarified` devuelve la spec a `draft`.

## 8. Excepciones

### Etapa 1 (bootstrap)

La única rama que puede existir sin spec previa es la que crea la constitución y el protocolo. Autorizada una sola vez por el propietario y registrada en `CHANGELOG.md`.

### Cambio editorial

Sin spec solo se permite un cambio **exclusivamente editorial** (erratas, formato, enlaces) que no altere comportamiento, configuración, requisitos ni scripts. Debe ir en commit `docs:` o `chore:`.

Un hotfix exige spec, aunque sea mínima.

## 9. Validador determinista

`tools/sdd/validate.py` es el árbitro. Uso:

```bat
python tools\sdd\validate.py --all
python tools\sdd\validate.py --spec SPEC-001 --gate G1
python tools\sdd\validate.py --spec SPEC-001 --gate G4 --git
python tools\sdd\validate.py --next-id
```

Comprobaciones: frontmatter, estados, secciones, EARS, IDs únicos, cobertura `RF/CB → CA → T`, dependencias acíclicas, estimaciones, ausencia de rutas técnicas en `spec.md`, `clarify.md` cerrado, reporte al 100 %, consistencia con `specs/INDEX.md`, longitud de `AGENTS.md`, y con `--git`: rama, diff dentro del alcance y commits con `Spec: SPEC-NNN`.

Códigos de salida: `0` válido, `1` error de validación, `2` error de uso.

## 10. Agentes y permisos

| Agente | Rol | Permisos |
|---|---|---|
| `sdd` | Orquestador, estado y diagnóstico | Solo lectura; puede lanzar subagentes |
| `planner` | Spec, clarify, plan, tasks | Escribe solo `specs/**` |
| `coder` | TDD tarea por tarea | Escribe `src/**`, `tests/**`, `tools/**`, `tasks.md` |
| `reviewer` | Auditoría independiente | Solo lectura de código; escribe solo `validation_report.md` |
| `documenter` | Correcciones editoriales y normativas | Escribe solo `docs/**` y `AGENTS.md`; sin terminal ni subagentes |

Las skills (`sdd-lifecycle`, `ears-spec`, `sdd-plan-tasks`, `tdd-implement`, `llama-validation`) cargan el procedimiento detallado bajo demanda; `AGENTS.md` no las duplica.
