# Interacción de Subagentes en OpenCode (`@planner`, `@coder`, `@reviewer`)

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

Diagrama de secuencia que ilustra el aislamiento de ventanas de contexto, el principio de menor privilegio, el bucle TDD agéntico y la integración con servidores MCP dentro del ciclo SDD.

```mermaid
%% ============================================================================
%% TÍTULO: Interacción de Subagentes en OpenCode (@planner, @coder, @reviewer)
%% DESCRIPCIÓN: Flujo de contexto aislado, menor privilegio, bucle TDD y MCP
%% ============================================================================
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'actorBkg': '#0F172A',
    'actorTextColor': '#F8FAFC',
    'actorBorder': '#38BDF8',
    'signalColor': '#475569',
    'signalTextColor': '#0F172A',
    'labelBoxBkgColor': '#F1F5F9',
    'labelBoxBorderColor': '#94A3B8',
    'loopTextColor': '#0F172A',
    'noteBkgColor': '#FFFBEB',
    'noteBorderColor': '#D97706',
    'noteTextColor': '#78350F'
  }
}}%%
sequenceDiagram
    autonumber
    actor Dev as Desarrollador / Orquestador
    participant Planner as "@planner<br/>(Menor Privilegio: Read-Only)"
    participant Coder as "@coder<br/>(Ventana Contexto Aislada)"
    participant Reviewer as "@reviewer<br/>(Auditoría Sin Sesgo)"
    participant Repo as "Repositorio Git &<br/>Servidores MCP"

    %% FASE 1: PLANIFICACIÓN
    rect rgb(255, 251, 235)
        Note over Dev, Repo: FASE 1: Planificación Técnica y Tareas Atómicas (Etapas 4 y 5)
        Dev->>Planner: Invoca planificación con spec.md y clarify.md
        activate Planner
        Planner->>Repo: Lee docs/constitution.md y AGENTS.md
        Planner->>Repo: Consulta docs técnicas en tiempo real (MCP Context7)
        Repo-->>Planner: Esquemas, contratos y reglas de dominio
        Planner->>Repo: Redacta specs/NNN-slug/plan.md y tasks.md
        Planner-->>Dev: Entrega plan técnico y checklist atómico
        deactivate Planner
    end

    %% FASE 2: IMPLEMENTACIÓN TDD
    rect rgb(255, 241, 242)
        Note over Dev, Repo: FASE 2: Bucle de Implementación TDD Agéntico (Etapa 6)
        Dev->>Coder: Asigna ejecución de tasks.md (Contexto limpio)
        activate Coder
        loop Por cada tarea atómica en tasks.md (15-30 min)
            Coder->>Repo: Fase Roja: Escribe test unitario según spec.md
            Repo-->>Coder: Test falla (Confirmación esperada)
            Coder->>Repo: Fase Verde: Implementa código mínimo
            Repo-->>Coder: Test pasa
            Coder->>Repo: Refactoriza, ejecuta linters y marca [x] en tasks.md
        end
        Coder-->>Dev: Notifica 100% de tareas completadas
        deactivate Coder
    end

    %% FASE 3: VALIDACIÓN SIN SESGO
    rect rgb(236, 253, 245)
        Note over Dev, Repo: FASE 3: Auditoría Independiente y Convergencia (Etapa 7)
        Dev->>Reviewer: Solicita auditoría (Sin historial previo de @coder)
        activate Reviewer
        Reviewer->>Repo: Lee spec.md, constitution.md y diff de código
        Reviewer->>Repo: Ejecuta validación E2E (MCP Playwright / Chrome DevTools)
        Reviewer->>Repo: Verifica esquemas en BD (MCP PostgreSQL / Supabase)
        Repo-->>Reviewer: Resultados de contract testing y trazabilidad
        Reviewer->>Repo: Genera specs/NNN-slug/validation_report.md

        alt Convergencia < 100% (Brechas o alucinaciones detectadas)
            Reviewer-->>Dev: Rechaza y reporta hallazgos trazables
            Dev->>Coder: Reabre tareas específicas para corrección
        else Convergencia certificada al 100%
            Reviewer-->>Dev: Aprueba certificación SDD
            Dev->>Repo: Commit y sincronización final en Git
        end
        deactivate Reviewer
    end
```
