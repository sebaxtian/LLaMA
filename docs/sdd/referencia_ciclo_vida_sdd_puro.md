# **Guía de Referencia: Ciclo de Vida del Desarrollo Basado en Especificaciones (SDD) Puro**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)** es una metodología de ingeniería de software en la que una especificación formal, estructurada y legible por máquina actúa como la guía o fuente única de verdad del sistema antes de escribir código ejecutable.

A diferencia de la programación basada en _prompts_ informales (_vibe coding_), el SDD puro establece una separación estricta entre el **QUÉ** se construye y el **CÓMO** se implementa, estructurando el proceso en un ciclo de vida cerrado de **7 etapas secuenciales**.

---

## **1\. Diagrama de Flujo del Ciclo de Vida SDD (7 Etapas)**

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • docs/constitution.md (Principios innegociables y guardrails)         │
 │  • AGENTS.md (Límites operativos del repositorio y System Prompt)       │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 2: ESPECIFICACIÓN (Specify)                     │
 │  • specs/NNN-slug/spec.md (Requisitos de negocio en notación EARS)     │
 │  • Define el QUÉ y el POR QUÉ (Lógica pura, aislado de código)          │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                    ETAPA 3: CLARIFICACIÓN (Clarify)                       │
 │  • specs/NNN-slug/clarify.md (Auditoría QA / Inspección de puntos ciegos)│
 │  • Q&A interactivo, resolución de ambigüedades y casos borde              │
 └────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                  ETAPA 4: PLANIFICACIÓN TÉCNICA (Plan)                  │
 │  • specs/NNN-slug/plan.md (Diseño técnico, arquitectura y esquemas)    │
 │  • Define el CÓMO (JSON Schema, SQL, DTOs, módulos, contratos API)      │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 5: TAREAS ATÓMICAS (Tasks)                      │
 │  • specs/NNN-slug/tasks.md (Desglose en unidades ejecutables acotadas) │
 │  • Secuencia de trabajo TDD con casillas de verificación (- [ ])        │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 6: IMPLEMENTACIÓN (Implement)                   │
 │  • Bucle agéntico TDD (Red -> Green -> Refactor) por tarea              │
 │  • Generación de pruebas automatizadas y código de producción           │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 7: VALIDACIÓN (Validate)                       │
 │  • specs/NNN-slug/validation_report.md (Pruebas de contrato y auditoría)│
 │  • Verificación de matriz EARS y análisis de convergencia                │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                         ¿CONVERGENCIA AL 100%?
                         /                     \
                      SÍ                        NO
                      /                          \
                     ▼                            ▼
         ┌───────────────────────┐    ┌──────────────────────────┐
         │ Integración / Merge   │    │ Retroalimentación SDD    │
         │ (Spec-Anchored Live)  │    │ (Ajustar Spec/Plan/Tasks)│
         └───────────────────────┘    └──────────────────────────┘
```

---

## **2\. Desglose Estructurado Etapa por Etapa**

| Etapa                  | Artefacto Clave             | Pregunta Principal                       | Responsable / Rol    | Resultado Esperado                                                                     |
| :--------------------- | :-------------------------- | :--------------------------------------- | :------------------- | :------------------------------------------------------------------------------------- |
| **1\. Constitución**   | `constitution.md AGENTS.md` | ¿Cuáles son las reglas innegociables?    | Arquitecto / Equipo  | Límites arquitectónicos, stack permitido y guardrails operativos.                      |
| **2\. Especificación** | `spec.md`                   | ¿Qué problema resolvemos y por qué?      | Product Owner / IA   | Requisitos funcionales en notación EARS y criterios de aceptación.                     |
| **3\. Clarificación**  | `clarify.md`                | ¿Qué puntos ciegos o casos borde faltan? | QA Auditor / IA      | Resolución de ambigüedades, reglas deterministas, Q\&A de negocio y parches a la spec. |
| **4\. Planificación**  | `plan.md`                   | ¿Cómo se diseña técnicamente?            | Líder Técnico / IA   | Estructura de módulos, JSON Schemas, contratos API y ADRs.                             |
| **5\. Tareas**         | `tasks.md`                  | ¿Cómo dividimos el trabajo en bloques?   | Agente Planner / Dev | Lista de tareas atómicas (15–30 min) enlazadas a IDs de requisitos.                    |
| **6\. Implementación** | Código Fuente \+ Tests      | ¿Cómo ejecutamos cada tarea en TDD?      | Agente Coder / Dev   | Prueba unitaria (Red), código mínimo (Green) y actualización de checkboxes (`- [x]`).  |
| **7\. Validación**     | `validation_report.md`      | ¿El software cumple el contrato al 100%? | Subagente Reviewer   | Reporte de convergencia, matriz de trazabilidad y CI/CD contract tests.                |

---

## **3\. Guía Paso a Paso y Estructura de Artefactos**

### **Etapa 1: Constitución del Repositorio (`constitution.md` y `AGENTS.md`)**

Establece las directrices globales del repositorio antes de iniciar cualquier desarrollo.

- **`docs/constitution.md`**: Define las normas arquitectónicas de alto nivel, separación de capas (dominio aislado de adaptadores) y restricciones de librerías permitidas.
- **`AGENTS.md`**: Actúa como la guía de contexto operativo (_System Prompt_ del repositorio) para los agentes de codificación, indicando comandos de test, linters y prohibiciones explícitas.

```
# AGENTS.md (Ejemplo base)
## Stack Tecnológico y Restricciones
- Python 3.12 con tipado estricto (mypy --strict).
- No añadir dependencias de I/O a la capa de dominio.

## Comandos Principales
- Tests: `pytest tests/`
- Linter: `ruff check .`
```

---

### **Etapa 2: Especificación Funcional (`spec.md`)**

Define la intención del producto y la lógica de negocio sin mezclar detalles de código, rutas de archivos ni infraestructura técnica. Para asegurar que los requisitos sean deterministas y verificables, se redactan utilizando la notación **EARS** (_Easy Approach to Requirements Syntax_):

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                       PATRONES SINTÁCTICOS EARS                         │
 ├─────────────────────────────────────────────────────────────────────────┤
 │ 1. Ubicuo (Siempre activo):                                             │
 │    • "El <sistema> debe <respuesta>"                                    │
 │                                                                         │
 │ 2. Dirigido por Eventos:                                                │
 │    • "Cuando <evento desencadenante>, el <sistema> debe <respuesta>"    │
 │                                                                         │
 │ 3. Dirigido por Estados:                                                │
 │    • "Mientras <estado activo>, el <sistema> debe <respuesta>"          │
 │                                                                         │
 │ 4. Característica Opcional:                                             │
 │    • "Donde <opción habilitada>, el <sistema> debe <respuesta>"         │
 │                                                                         │
 │ 5. Comportamiento No Deseado / Excepción:                               │
 │    • "Si <error o condición no deseada>, entonces el <sistema> debe..." │
 └─────────────────────────────────────────────────────────────────────────┘
```

&nbsp;

```
# specs/NNN-slug/spec.md (Ejemplo base)
## 1. Contexto y Objetivo
Descripción del problema de negocio.

## 2. Requisitos Funcionales (EARS)
- **RF-001 (Evento):** Cuando [evento], el [sistema] debe [respuesta].
- **RF-002 (Excepción):** Si [condición no deseada], entonces el [sistema] debe [respuesta].

## 3. Casos Borde y Fuera de Alcance
- **CB-001:** [Escenario límite].
- **Fuera de Alcance:** [Lo que explícitamente no se implementará].
```

---

### **Etapa 3: Clarificación (`clarify.md`)**

Auditoría previa al diseño técnico para resolver ambigüedades, vacíos de especificación o escenarios no contemplados mediante preguntas y respuestas directas.

```
# specs/NNN-slug/clarify.md (Ejemplo base)
## 1. Hallazgos y Ambigüedades
- **AMB-001:** [Inconsistencia detectada en spec.md].

## 2. Decisiones de Negocio (Q&A)
- **Pregunta:** ¿Cómo responder ante datos duplicados?
- **Decisión:** Rechazar la operación emitiendo error 409.

## 3. Parches a spec.md
- [x] RF-002 actualizado con la decisión tomada.
```

---

### **Etapa 4: Planificación Técnica y Arquitectura (`plan.md`)**

Traduce los requisitos funcionales en diseño técnico formal, esquemas de datos y contratos de componentes.

````
# specs/NNN-slug/plan.md (Ejemplo base)
## 1. Arquitectura de Módulos
- `src/core/domain.py`: Lógica pura de negocio.
- `src/storage/repo.py`: Persistencia.

## 2. Esquema de Datos (JSON Schema / SQL)
```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "titulo": { "type": "string", "minLength": 1 }
  },
  "required": ["id", "titulo"]
}
```
## 3. Interfaces y Estrategia de Testing
- Pruebas unitarias para validar algoritmos de sanitización y modelos de dominio.
````

---

### **Etapa 5: Descomposición en Tareas Atómicas (`tasks.md`)**

Convierte la arquitectura técnica en una lista de tareas pequeñas, ordenadas por dependencias y diseñadas para procesarse en sesiones acotadas de desarrollo.

```
# specs/NNN-slug/tasks.md (Ejemplo base)
- [ ] **Tarea 1: Modelo de dominio y validaciones**
  - **Depende de:** Ninguna
  - **Requisitos:** RF-001
  - **Criterio de Aceptación:** Test unitario `test_model_validation` pasando.

- [ ] **Tarea 2: Adaptador de almacenamiento**
  - **Depende de:** Tarea 1
  - **Requisitos:** RF-002, CB-001
  - **Criterio de Aceptación:** Persistencia validada con tests de integración.
```

---

### **Etapa 6: Implementación Guiada (`Implement`)**

Ejecución del trabajo tarea por tarea bajo un flujo estricto de Desarrollo Guiado por Pruebas (TDD):

1. **Red:** Escribir la prueba automatizada que cubra el requisito `RF-xxx` y verificar que falle.
2. **Green:** Escribir el código mínimo de producción para que la prueba pase.
3. **Refactor:** Limpiar el código respetando los linters y la constitución del proyecto.
4. **Checkbox:** Actualizar la tarea en `tasks.md` a marcada (`- [x]`) y proceder con la siguiente unidad.

---

### **Etapa 7: Validación de Contrato y Cierre (`Validate`)**

Auditoría final del sistema completo para certificar la convergencia entre la especificación y el código entregado.

```
# specs/NNN-slug/validation_report.md (Ejemplo base)
## 1. Matriz de Trazabilidad de Requisitos
| ID Requisito | Criterio EARS | Prueba Automatizada | Estado |
| :--- | :--- | :--- | :--- |
| **RF-001** | Creación válida | `tests/test_core.py::test_create` | PASADO |
| **RF-002** | Manejo de error | `tests/test_core.py::test_error` | PASADO |

## 2. Dictamen de Convergencia
- [x] **CONVERGIDO:** El código cumple al 100% con los criterios de aceptación. Listo para merge.
```

---

## **4\. Taxonomía de Adopción de SDD**

El compromiso con la especificación una vez generado el código define el modelo de adopción del equipo:

```
      BAJO COMPROMISO <─────────────────────────────────────────> ALTO COMPROMISO

 ┌────────────────────────┐   ┌─────────────────────────┐   ┌────────────────────────┐
 │       Spec-First       │   │     Spec-Anchored       │   │     Spec-as-Source     │
 ├────────────────────────┤   ├─────────────────────────┤   ├────────────────────────┤
 │ • La spec arranca el   │   │ • La spec y el código   │   │ • La spec es la ÚNICA  │
 │   desarrollo.          │   │   conviven y evolucionan│   │   fuente editada.      │
 │ • La spec puede        │   │   juntos en Git.        │   │ • El código se         │
 │   obsoletearse post-   │   │ • Doble fuente de       │   │   regenera al 100%     │
 │   generación.          │   │   verdad sincronizada.  │   │   vía compiladores/IA. │
 │ • Ideal para PoCs.     │   │ • Ideal para Enterprise │   │ • Ideal para SDKs.     │
 └────────────────────────┘   └─────────────────────────┘   └────────────────────────┘
```

---

## **5\. Matriz Comparativa: Vibe Coding vs. SDD Puro**

| Criterio                | Programación Imprecisa (_Vibe Coding_)                  | Desarrollo Basado en Especificaciones (SDD)          |
| :---------------------- | :------------------------------------------------------ | :--------------------------------------------------- |
| **Punto de Inicio**     | Prompts informales y ad-hoc.                            | Especificación formal previa (`spec.md` / OpenAPI).  |
| **Fuente de Autoridad** | El código generado por la IA.                           | La especificación aprobada y la Constitución.        |
| **Revisión de Calidad** | Aceptación a ciegas del output.                         | Auditoría previa en plan y posterior en validación.  |
| **Manejo de Cambios**   | Re-promptear y parchar el código.                       | Actualizar la spec primero y regenerar/refactorizar. |
| **Riesgo Principal**    | Alucinaciones, deuda técnica y _intent drift_.          | Inversión de tiempo en el análisis inicial.          |
| **Caso de Uso Ideal**   | Prototipos desechables y scripts de una sola ejecución. | Software empresarial, microservicios y producción.   |

---

## **6\. Integración Operacional con Entornos Agénticos (OpenCode)**

En **OpenCode**, el flujo SDD se ejecuta mediante la combinación de sus modos primarios, comandos agénticos y extensiones modulares:

```
               ┌──────────────────────────────────────────┐
               │         SESIÓN OPENCODE (Terminal)       │
               └────────────────────┬─────────────────────┘
                                    │
             ┌──────────────────────┴──────────────────────┐
             │                                             │
             ▼                                             ▼
 ┌───────────────────────┐                     ┌───────────────────────┐
 │       PLAN MODE       │                     │      BUILD MODE       │
 │   (Shift + Tab / TUI) │                     │     (Ejecución)       │
 ├───────────────────────┤                     ├───────────────────────┤
 │ • Lee AGENTS.md       │                     │ • Lee tasks.md        │
 │ • Genera spec.md      │                     │ • Ejecuta bucle TDD   │
 │ • Audita clarify.md   │                     │ • Modifica código     │
 │ • Diseña plan.md      │                     │ • Lanza pytest/vitest │
 │ • Crea tasks.md       │                     │ • Marca casillas [x]  │
 └───────────────────────┘                     └───────────────────────┘
             │                                             │
             └──────────────────────┬──────────────────────┘
                                    │
                                    ▼
               ┌──────────────────────────────────────────┐
               │         MODULARIDAD & MCP SERVERS        │
               ├──────────────────────────────────────────┤
               │ • .agents/skills/ (Habilidades SDD)      │
               │ • .opencode/commands/ (/spec, /implement)│
               │ • Context7 MCP (Documentación técnica)   │
               │ • Subagentes (@planner, @review, @coder) │
               └──────────────────────────────────────────┘
```

---
