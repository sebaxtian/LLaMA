# Corpus SDD — Índice y estado

Esta carpeta contiene la documentación de referencia y la norma ejecutable del Desarrollo Basado en Especificaciones (SDD) del proyecto `LLaMA`.

## Estado normativo

- **Norma ejecutable:** `PROTOCOLO_OPERATIVO.md` (rango 3 en la jerarquía).
- **Norma suprema:** `../constitution.md` (rango 1).
- **Operativo para agentes:** `../../AGENTS.md` (rango 2).
- El resto de documentos de esta carpeta son **corpus de referencia**: material explicativo y de fundamentos, no normativo. Ante contradicción, prevalece el `PROTOCOLO_OPERATIVO.md`.

## Orden de lectura recomendado

1. `PROTOCOLO_OPERATIVO.md` — la norma ejecutable que rige el trabajo.
2. `compendio_sdd.md` — fundamentos y taxonomía (Spec-First / Spec-Anchored / Spec-as-Source).
3. `referencia_7_etapas_sdd.md` — el ciclo de vida de 7 etapas.
4. `guia_constitution_md.md` — fundamentos de la constitución.
5. `guia_agents_md.md` — directrices para `AGENTS.md`.
6. `guia_metodo_ears_sdd.md` — notación EARS.
7. `guia_spec_md.md` — contrato de `spec.md`.
8. `guia_clarify_md.md` — contrato de `clarify.md`.
9. `guia_plan_md.md` — contrato de `plan.md`.
10. `guia_tasks_md.md` — contrato de `tasks.md`.
11. `guia_fase_implement_tdd.md` — protocolo TDD de implementación.
12. `guia_subagentes_opencode_sdd.md` — agentes `planner`/`coder`/`reviewer`.
13. `guia_skills_agentes_sdd.md` — skills y divulgación progresiva.
14. `guia_servidores_mcp.md` — servidores MCP.
15. `evolucion_sdlc_a_sdd.md` — evolución SDLC → SDD.

## Diagramas

- `mapa_mental_sdd.md` — mapa mental (Mermaid).
- `diagrama_flujo_ciclo_vida_sdd.md` — flujo del ciclo de vida.
- `diagrama_secuencia_subagentes_sdd.md` — secuencia de subagentes.
- `referencia_ciclo_vida_sdd_puro.md` — referencia extendida del ciclo.

## Plantillas

Las plantillas normativas de artefactos viven en `plantillas/`:

```text
plantillas/
├── spec.md
├── clarify.md
├── plan.md
├── tasks.md
└── validation_report.md
```

Los artefactos reales de cada feature viven en `specs/NNN-slug/`.

## Correcciones aplicadas al corpus

Este corpus se normalizó para alinearse con el protocolo:

- `-mpc` → `-mcp` (convención de nombres MCP del proyecto).
- IDs de 2 dígitos (`AMB-01`, `CB-01`) → 3 dígitos (`AMB-001`, `CB-001`).
- `specs/feature/` y `specs/001-feature/` → `specs/NNN-slug/`.
- Nombre único del reporte: `validation_report.md`.
- Reviewer: solo lectura sobre código; escribe únicamente `validation_report.md`.
- Los ejemplos de código de la documentación son ilustrativos, no normativos.
