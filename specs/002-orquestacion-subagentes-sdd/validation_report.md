# Reporte de validación - SPEC-002

## Entorno

- Sistema operativo: Windows 11.
- Rama: `feat/orquestacion-subagentes-sdd`.
- Commit auditado: `e7969d3e8e97f0e1722025a500b6dd6f923366b6`, «docs(spec): corregir evidencia de delegación de SPEC-002».
- Spec auditada: `spec.md` v0.10.0, `status: implemented`. Artefactos: `clarify.md` (AMB-001 a AMB-009), `plan.md` (DEC-001 a DEC-008), `tasks.md` (T-001 a T-010).
- Árbol de trabajo: `git status --short` muestra solo `?? specs/002-orquestacion-subagentes-sdd/validation_report.md` (este reporte). `git diff --check` sin hallazgos (código `0`).
- Herramientas: Git 2.56.0.windows.3, Python 3.15.2, OpenCode v2.3.0, validador `tools/sdd/validate.py`.
- Auditoría previa: `b7fe653`, NO CONVERGIDO por B-08 (evidencia de CA-001 y CA-002 apuntaba a una sesión fallida).
- Fecha de la auditoría: 2026-11-13. Auditor: subagente `reviewer`, independiente de `planner`, `coder` y `sdd`.
- Alcance de lectura: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md` (§2, §6, §7, §10), `spec.md`, `clarify.md`, `plan.md`, `tasks.md`, `.opencode/agents/{sdd,planner,coder}.md`, `.opencode/commands/sdd-*.md`, `CHANGELOG.md`, `specs/INDEX.md`, `git show e7969d3`, la API de sesiones (`/api/session`, `/api/session/{id}/message`) y los mensajes de las cuatro sesiones citadas y de la sesión orquestadora `ses_e2a83d57cffeiCv6HiuhGltNu9`.

### Configuración efectiva (API del servidor OpenCode)

Consultas ejecutadas con `location[directory]=C:\Users\sebax\Documents\Workspaces\LLaMA` (`opencode api get '/api/agent?...'`, `/api/agent/sdd`, `/api/agent/planner`, `/api/agent/coder`), código de salida `0`:

| Verificación | Resultado en la configuración cargada | Estado |
|---|---|---|
| `mode` por agente | `sdd | primary`, `planner | all`, `coder | all`, `reviewer | subagent`, `explore | subagent` | Conforme a AMB-001 y DEC-001 |
| `sdd`: `subagent` | `subagent * deny`, después `allow` para `planner`, `coder`, `reviewer` y `explore` | Conforme a RF-001, RF-004 |
| `sdd`: `edit` | `edit * deny`; ninguna regla `edit` con `allow` | Conforme a RF-005 |
| `sdd`: `shell` | Base `git push *` y `git tag *` en `ask`; luego `shell * ask`; después `allow` en este orden: `git status *`, `git diff *`, `git log *`, `git show *`, `git rev-parse *`, `git branch --show-current`, `git branch --all *`, `git add *`, `git commit *`, `python tools\sdd\validate.py *` | Lista idéntica a AMB-006 y DEC-007. Regla general antes de excepciones (RNF-001) |
| `planner`: `subagent` | `subagent * deny` como última regla de su lista propia; `edit * deny` seguido de `edit specs/** allow` | Conforme a RF-004, RNF-001 |
| `coder`: `subagent` y `edit` | `subagent * deny` como última regla; `edit specs/** deny`, `edit docs/** deny`, después `edit specs/*/tasks.md allow` | Conforme a RF-004, RNF-001 |

Nota de evaluación: la última regla coincidente gana (DEC-002 y DEC-007). Cualquier comando de `shell` no listado resuelve a `ask`.

### Comandos `sdd-*` (CA-006)

- `sdd-spec`, `sdd-clarify`, `sdd-plan`, `sdd-tasks` declaran `agent: planner`; `sdd-implement` declara `agent: coder`; `sdd-validate` declara `agent: reviewer`; `sdd-status` y `sdd-check` declaran `agent: sdd`.

### Verificación de la delegación real (CA-001, CA-002)

Sesión orquestadora `ses_e2a83d57cffeiCv6HiuhGltNu9` (agente `sdd`, «Ejecutar subagentes desde Sdd»). Las cuatro sesiones citadas en `tasks.md` son hijas de ella y su último turno es `succeeded`:

| Sesión | Agente | Último turno | Turnos (`idle`) | Ediciones verificadas en la sesión |
|---|---|---|---|---|
| `ses_e2a57522dffeRRIkHak1lRKfgp` | `planner` | `succeeded` | 1 | `clarify.md` (5), `plan.md` (3), `spec.md` (2), `tasks.md` (2), `INDEX.md` (1) |
| `ses_e2a5440c4ffeNYOxtM6zwgOvOP` | `planner` | `succeeded` | 1 | `spec.md` (2), `tasks.md` (1), `INDEX.md` (1) |
| `ses_e2a65fccdffeub1UpD5YFQA9cC` | `coder` | `succeeded` (3 de 3) | 3 | `.opencode/agents/sdd.md` (4), `planner.md`, `coder.md`, `tasks.md` (7) |
| `ses_e2a55d9c4ffe7V95BmavPV7hEg` | `coder` | `succeeded` (3 de 3) | 3 | `.opencode/agents/sdd.md` (3), `CHANGELOG.md` (1), `tasks.md` (8) |

Las cuatro sesiones coinciden con lo que se declara en `tasks.md`. La sesión `ses_e2a65fcc` tiene 50 mensajes, que es el límite de la respuesta de la API; su primer turno (T-006) queda fuera de la ventana visible (observación O-19).

Sesiones no citadas en los artefactos: `ses_e2a69fdefffe45VbPSPIvaSGKN` (planner) tiene tres turnos `succeeded` con 28 ediciones y un último turno `failed` (`provider.free-limit`, HTTP 429). Ningún artefacto de la spec la cita (verificado con búsqueda de identificadores en `spec.md`, `clarify.md`, `plan.md` y `tasks.md`). Corrección a la auditoría anterior: esta sesión no era «sin salida»; la exclusión de AMB-009 se basa en su último turno fallido, como describe AMB-009 (observación O-18).

### Salida del validador determinista

```text
> python tools\sdd\validate.py --spec SPEC-002 --gate G4 --git
OK: sin hallazgos.
código de salida: 0

> python tools\sdd\validate.py --all
OK: sin hallazgos.
código de salida: 0

> python tools\sdd\validate.py --spec SPEC-002 --gate G2
OK: sin hallazgos.
código de salida: 0
```

El código `0` no acredita convergencia: el validador acepta cualquier reporte que contenga la subcadena `CONVERGIDO`, incluido «NO CONVERGIDO» (O-01). El dictamen se decide con la matriz de este reporte.

## Matriz de trazabilidad

### Requisitos: RF, RNF, CB

| Requisito | CA | Prueba / comando | Evidencia | Estado |
|---|---|---|---|---|
| RF-001 | CA-001 | `/api/agent/sdd`: `subagent` allow para `planner`, `coder`, `reviewer`, `explore` | Sesiones hijas de `ses_e2a83d57` con agente `planner` (`ses_e2a57522`, `ses_e2a5440c`), `coder` (`ses_e2a65fcc`, `ses_e2a55d9c`) y `reviewer` (p. ej. `ses_e2a4feba`) | PASADO |
| RF-002 | CA-001, CA-006 | `/api/agent/planner`: `mode: all`; `sdd-spec`, `sdd-clarify`, `sdd-plan`, `sdd-tasks` con `agent: planner` | `ses_e2a57522` (planner, `succeeded`, edita `plan.md` tres veces); `ses_e2a5440c` (planner, `succeeded`) | PASADO |
| RF-003 | CA-002, CA-006 | `/api/agent/coder`: `mode: all`; `sdd-implement` con `agent: coder` | `ses_e2a65fcc` y `ses_e2a55d9c` (coder, tres turnos `succeeded` cada una) | PASADO |
| RF-004 | CA-003 | `/api/agent/sdd`: `subagent * deny` seguido de `allow` solo para cuatro agentes | Orden efectivo verificado en la configuración cargada (no se ejecutó un lanzamiento real denegado; O-17) | PASADO |
| RF-005 | CA-004 | `/api/agent/sdd`: `edit * deny` sin `allow` de edición | Denegación verificada en configuración. Riesgo residual vía `shell` (O-05) | PASADO |
| RF-006 | CA-005, CA-007 | `sdd.md` fila 6 «G2 verificada (`--gate G2`)» y regla 1; `validate.py --spec SPEC-002 --gate G2` | Código `0`. Texto de `sdd.md` verificado en la API. «aprobada» de `spec.md` leído como «verificada» (AMB-008; O-10) | PASADO |
| RF-007 | CA-008 | Seis plantillas de «Solicitudes» en `sdd.md`; prompts reales de `sdd` | Plantillas: spec, `Etapa: <etapa>` y resultado en las seis. Prompts reales (11 delegaciones de `ses_e2a83d57`): resultado esperado en 11 de 11; `SPEC-002` literal en 8 y por ruta en 2; la etapa se infiere del verbo, sin literal `Etapa:` (O-16) | PASADO (con observación O-16) |
| RNF-001 | CA-009 | `/api/agent`, `/api/agent/sdd`, `/api/agent/planner`, `/api/agent/coder` | Reglas generales antes de excepciones; cada regla declara `action`, `resource` y `effect` | PASADO |
| RNF-002 | CA-010 | `CHANGELOG.md`, `## [Unreleased]` | Sección sin cambios desde `b7fe653`; describe la configuración final (`shell *` `ask` con allowlist, `subagent * deny` en `planner` y `coder`, `mode: all`) | PASADO |
| CB-001 | CA-005 | `sdd.md` fila 6 y regla 2 | Precondición de Implement con G2 verificada; ninguna precondición de Implement cita G4 | PASADO |
| CB-002 | CA-008 | `sdd.md` regla 6 | Bloqueo registrado y propietario consultado | PASADO |
| CB-003 | CA-007 | `sdd.md` regla 1 | Registro del código de salida y parada si es distinto de `0` | PASADO |

Resumen de la matriz de requisitos: 12 requisitos (RF-001 a RF-007, RNF-001, RNF-002, CB-001 a CB-003). **PASADO: 12 de 12 (100 %).** PENDIENTE: 0.

### Criterios de aceptación: CA-001 a CA-010

| CA | Cubre | Prueba / evidencia | Estado |
|---|---|---|---|
| CA-001 | RF-001, RF-002 | Configuración de `/api/agent/sdd` y `/api/agent/planner`; sesiones planner `ses_e2a57522` y `ses_e2a5440c` (hijas de `sdd`, `succeeded`, editan `plan.md`, `clarify.md`, `spec.md` y `tasks.md`). La evidencia registrada en `tasks.md` coincide con estas sesiones | PASADO |
| CA-002 | RF-003 | Configuración de `/api/agent/coder`; sesiones coder `ses_e2a65fcc` y `ses_e2a55d9c` (hijas de `sdd`, `succeeded`) | PASADO |
| CA-003 | RF-004 | `/api/agent/sdd`: `subagent * deny` seguido de `allow` solo para cuatro agentes | PASADO |
| CA-004 | RF-005 | `/api/agent/sdd`: `edit * deny` | PASADO |
| CA-005 | RF-006, CB-001 | `sdd.md`: fila 6 y regla 2 con G2 verificada | PASADO |
| CA-006 | RF-002, RF-003 | `/api/agent`: `planner` y `coder` con `mode: all`; comandos `sdd-*` con `agent:` correspondiente | PASADO |
| CA-007 | RF-006, CB-003 | `sdd.md` regla 1: registro del código de salida y parada si es distinto de `0` | PASADO |
| CA-008 | RF-007, CB-002 | Plantillas con spec, etapa y salida; regla 6 con bloqueo registrado | PASADO |
| CA-009 | RNF-001 | Orden de reglas verificado en las cuatro listas de permisos consultadas | PASADO |
| CA-010 | RNF-002 | Entrada en `CHANGELOG.md` `[Unreleased]` con la configuración final | PASADO |

Resumen de CA: **10 de 10 PASADO.**

### Trazabilidad de cobertura

- `RF/CB → CA`: completa. Los doce requisitos tienen al menos un CA; cada CA declara «Cubre:».
- `RF/CB → T`: completa según el validador (`--gate G2`, `--all` y `--gate G4 --git`, sin hallazgos).
- `CA → T`: implícita. `tasks.md` no cita identificadores CA (O-07).
- `evidencia`: las cuatro sesiones citadas existen y coinciden con su `tasks.md`; ninguna cita sesiones fallidas.

## Cierre de brechas de auditorías previas (B-06 a B-09 y O-03)

| Brecha | Estado | Verificación en `e7969d3` |
|---|---|---|
| B-06 - `CHANGELOG.md` sin configuración final (RNF-002, CA-010) | CERRADA | `[Unreleased]` coincide con la configuración cargada; sin cambios en `e7969d3` |
| B-07 - allowlist de `shell` no registrada (AMB-006, DEC-007) | CERRADA | AMB-006 y DEC-007 listan las diez reglas que devuelve `/api/agent/sdd` |
| B-08 - evidencia de delegación real (CA-001, CA-002) | CERRADA | `tasks.md` cita solo cuatro sesiones hijas de `sdd` con `succeeded` y ediciones coherentes. `ses_e2a69…` no aparece en ningún artefacto de la spec. AMB-009 registra la decisión de sustitución de AMB-004 |
| B-09 - regla 1 de `sdd.md` sin código de salida (CA-007, CB-003) | CERRADA | La regla 1 exige registrar el código de salida y detenerse si es distinto de `0` |
| O-03 - «G2 aprobada» no verificable | CERRADA | AMB-008, DEC-006, fila 6 de `sdd.md` y regla 2 usan «G2 verificada». Residual de redacción en `spec.md` (O-10) |

Además, O-12 (reutilización de la sesión de `coder` entre tareas) queda resuelta por la regla de AMB-009: cada turno cuenta como invocación. Ver O-19 y O-22.

Brechas B-01 a B-05: cerradas en auditorías previas y sin regresión en `e7969d3` (verificadas en la configuración cargada).

## Brechas

**Ninguna brecha abierta.** Ninguno de los 12 requisitos ni de los 10 CA tiene evidencia no conforme.

## Observaciones

Observaciones sin efecto directo en el dictamen. Se registran para decisión del propietario o para trabajo posterior.

- **O-01 - El validador no distingue convergencia de no convergencia.** `tools/sdd/validate.py` busca la subcadena `CONVERGIDO` y acepta «NO CONVERGIDO» con código `0`. Fuera de esta spec (plan, «Alcance de la reapertura»).
- **O-02 - PROTOCOLO §6 pendiente de edición editorial.** §6 todavía define G4 como «autoriza la implementación». AMB-005 lo deja como cambio editorial posterior.
- **O-03 - Verificación de G2 no equivale a aprobación.** Cerrada. La verificación la hace el agente `sdd` con el validador; el validador no comprueba `tasked` por sí mismo.
- **O-04 - Correspondencia etapa → compuerta.** La tabla de precondiciones de `sdd.md` la indica por filas; suficiente.
- **O-05 - Riesgo residual de `shell` con `ask`.** Si el propietario aprueba un comando de escritura, `sdd` puede ejecutarlo (AMB-006).
- **O-06 - `planner` y `coder` sin restricción de `shell`.** Heredan `shell * allow` de la política base. Anterior a SPEC-002; candidato para una spec de permisos.
- **O-07 - Trazabilidad `CA → T` implícita.** `tasks.md` no cita identificadores CA; PROTOCOLO §3 exige la cadena completa.
- **O-08 - Detalle técnico en `spec.md`.** Menciona OpenCode V2, `permissions`, `action`, `resource`, `effect`, `CHANGELOG.md` y `opencode.jsonc`. Decisión del propietario sobre si se acepta como requisito de configuración.
- **O-09 - Artefactos de Clarify y Plan fuera de cualquier campo `Archivos`.** `clarify.md` y `plan.md` cambian en `b7fe653` y `e7969d3`, pero ninguna tarea los declara (PROTOCOLO §7). Higiene de alcance.
- **O-10 - Residual de «aprobada» en `spec.md`.** RF-006, CB-001 y CA-005 conservan «G2 aprobada»; AMB-008 los lee como «verificada con el validador». Si se quiere eliminar la ambigüedad, requiere una versión nueva de la spec.
- **O-11 - Causa de B-08 (identificadores no verificados en el prompt).** Causa ya corregida en `e7969d3`. Recomendación pendiente: que `sdd` compruebe con la API las evidencias antes de registrarlas.
- **O-13 - Validación de T-006 desactualizada.** El campo «Validación» de T-006 lista `git branch *` en la versión original; en `e7969d3` se corrigió a la lista de AMB-006. Registro histórico; la evidencia de T-006 sí registra la lista correcta.
- **O-14 - `git add *` y `git commit *` sin restricción de argumentos.** `git add .` puede preparar archivos no deseados. `.gitignore` mitiga el riesgo. Riesgo aceptado por la autorización del propietario.
- **O-15 - Historial de versiones.** Coherente: `spec.md` v0.10.0 `implemented`; el historial de `clarify.md` describe la reapertura v0.8.0.
- **O-16 - RF-007: literal de etapa en las delegaciones reales.** Las plantillas de `sdd.md` incluyen `Etapa: <etapa>`, pero las 11 delegaciones visibles de `ses_e2a83d57` no lo usan literalmente; la etapa se infiere del verbo («Audita», «Implementa», «Corrige»). El identificador de spec aparece como `SPEC-002` en 8 y por ruta en 2; una (ampliación de T-009) no lo incluye, pero es continuación de la misma tarea. El reviewer considera que la información necesaria está en cada solicitud y, por eso, RF-007 se marca PASADO. **Punto de decisión:** si el propietario interpreta RF-007 como exigencia del literal `Etapa:`, el dictamen pasaría a NO CONVERGIDO. Recomendación: que `sdd` use la plantilla literal en las siguientes delegaciones, o que el propietario lo aclare en `clarify.md`.
- **O-17 - Pruebas negativas de CA-003 y CA-004 solo por configuración.** La denegación de `subagent` a un agente no autorizado y la de `edit` desde `sdd` se verifican en la configuración efectiva; no se ejecutó un intento real. La prueba negativa manual del plan no se ha realizado.
- **O-18 - Corrección a la auditoría anterior.** `ses_e2a69fdefffe45VbPSPIvaSGKN` tenía tres turnos `succeeded` con ediciones. La afirmación de `b7fe653` de que «no produjo ningún artefacto» era inexacta. La exclusión de AMB-009 se basa en su último turno fallido, que es lo que dice AMB-009.
- **O-19 - Ventana de mensajes de la API.** `/api/session/{id}/message` devuelve como máximo 50 mensajes. En `ses_e2a65fcc` el primer turno (T-006) queda fuera de la ventana. Su evidencia descansa en `/api/agent/sdd`, en `tasks.md` y en el título de la sesión («Implementar T-006 shell acotado»).
- **O-20 - Referencias históricas a la TUI en `clarify.md`.** Hay cuatro menciones (líneas 55, 99, 101 y 130): el texto original de AMB-004 y la explicación de AMB-009. `spec.md`, `plan.md` y `tasks.md` no mencionan la TUI. AMB-004 no lleva una anotación explícita de «sustituido por AMB-009». Es registro de auditoría; recomendable anotarlo en un cambio editorial futuro.
- **O-21 - Atribución de AMB-009.** AMB-009 está atribuido a «Agent Sebaxtian» y la regla de §7 que introduce (cada turno de subagente es una invocación) es una interpretación de proceso. El reviewer no puede verificar externamente que el propietario la haya dictado. Se recomienda que el propietario la confirme al aprobar G4.
- **O-22 - Ampliación de T-009 en la misma sesión.** `ses_e2a55d9c` tiene tres turnos para dos tareas: T-009, una ampliación de T-009 pedida por el propietario («G2 se verifica») y T-010. La ampliación es una instrucción explícita del propietario (PROTOCOLO §7) y no altera el alcance.
- **O-23 - Estado `implemented` con G4 pendiente.** `spec.md` y `INDEX.md` están en `implemented`. Tras la aprobación de G4 del propietario, el estado debe pasar a `validated` según el ciclo del PROTOCOLO §2; no lo cambia este reporte.

## Dictamen

- [x] CONVERGIDO (100 % de requisitos con evidencia PASADO).
- [ ] NO CONVERGIDO.

Resumen: **12 de 12 requisitos (RF-001 a RF-007, RNF-001, RNF-002, CB-001 a CB-003) con evidencia PASADO (100 %); 10 de 10 CA PASADO.** Validador: `--spec SPEC-002 --gate G4 --git` código `0`; `--all` código `0`; `--spec SPEC-002 --gate G2` código `0`; `git diff --check` código `0`.

Estado de las brechas de la tercera ronda:

- B-06: CERRADA.
- B-07: CERRADA.
- B-08: CERRADA. El registro corregido cita sesiones hijas de `sdd` con `succeeded`; ninguna sesión fallida aparece en los artefactos.
- B-09: CERRADA.
- O-03: CERRADA.

Coherencia final (CB-001, CA-005, RF-006 y tabla de `sdd.md` frente a PROTOCOLO §2): la tabla de `sdd.md` coincide con §2. Implement (fila 6) exige G2 verificada y spec en `tasked`; G3 completa para Validate; G4 aparece solo al final de Validate (plantilla y regla 8). No hay G4 como precondición de Implement. El texto «G2 aprobada» de `spec.md` queda como residual de redacción (O-10).

Observaciones residuales que no bloquean la convergencia: O-16 (decisión sobre el literal de etapa, único punto cuya interpretación podría cambiar el dictamen), O-18 (corrección de la auditoría anterior), O-20 (referencias históricas a la TUI), O-21 (confirmación de AMB-009 por el propietario) y O-01 (el validador acepta «NO CONVERGIDO»).

El dictamen de este reporte no aprueba G4: la aprobación es exclusiva del propietario.

## Aprobación

- [ ] G4: `- Approved by: Agent Sebaxtian` (AAAA-MM-DD).

> El dictamen CONVERGIDO indica que la matriz cumple el 100 % de los requisitos con evidencia PASADO. No aprueba G4: la aprobación es exclusiva del propietario.
