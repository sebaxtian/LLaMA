---
name: sdd-lifecycle
description: Ciclo de vida SDD de 7 etapas, estados y compuertas del proyecto LLaMA. Úsala para navegar o diagnosticar el proceso SDD.
---

# Ciclo de vida SDD (7 etapas)

Carga esta skill para navegar el proceso completo del Desarrollo Basado en Especificaciones del proyecto.

## Etapas y artefactos

| Etapa | Artefacto | Estado |
|---|---|---|
| 1. Constitución / Setup | `constitution.md`, `AGENTS.md`, agentes, skills | — |
| 2. Specify | `spec.md` | `draft` |
| 3. Clarify | `clarify.md` + parches | `clarified` |
| 4. Plan | `plan.md` | `planned` |
| 5. Tasks | `tasks.md` | `tasked` |
| 6. Implement (TDD) | código + tests | `implementing` → `implemented` |
| 7. Validate | `validation_report.md` | `validated` |

## Estados

```text
draft → clarified → planned → tasked → implementing → implemented → validated → released
  └─────────┴───────────┴──────────┴──→ cancelled
validated → implementing (reapertura con motivo)
released / validated → superseded
```

## Compuertas

- **G1** — spec clara, sin ambigüedades, EARS correcto, aprobación del propietario.
- **G2** — plan y tasks conformes y con cobertura 100 %.
- **G3** — todas las tareas `[x]` con evidencia.
- **G4** — reporte converge al 100 % y aprobación de implementación.
- **G5** — integración Git `merge --no-ff` y rama eliminada.
- **G6** — release autorizado, tag anotado.

## Regla clave

Las transiciones son solo hacia adelante. Una reapertura exige motivo, incremento de versión y revalidación completa.
