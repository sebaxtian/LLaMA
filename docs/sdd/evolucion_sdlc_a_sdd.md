# **Evolución del Ciclo de Vida del Software: Del SDLC Clásico al SDD Moderno**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El **Ciclo de Vida del Desarrollo de Software (SDLC, _Software Development Life Cycle_) clásico** representa el marco metodológico tradicional que define las etapas secuenciales o iterativas por las que atraviesa un proyecto de software, desde su concepción inicial hasta su retiro.

En la ingeniería de software contemporánea, la irrupción de la Inteligencia Artificial y los agentes de codificación ha transformado este ciclo tradicional hacia el **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)** puro. Esta evolución no elimina la ingeniería de software, sino que la moderniza y perfecciona: sustituye los _prompts_ imprecisos (_vibe coding_) y la documentación retroactiva por **especificaciones estructuradas y legibles por máquina**, las cuales actúan como la fuente única de verdad para desarrolladores humanos y agentes de IA.

A continuación se detalla la comparativa y el mapeo fase por fase entre el **SDLC clásico** y su correspondiente contraparte en el **SDD moderno**.

---

## **1\. Mapeo Detallado de las Fases: SDLC Clásico vs. SDD Moderno**

### **Fase 1: Planificación y Alcance Inicial ➔ Constitución (_Setup / Constitution_)**

- **SDLC Clásico:** Durante esta fase preliminar, los líderes de proyecto, arquitectos y partes interesadas (_stakeholders_) identifican la problemática de negocio, analizan la viabilidad técnica y financiera, definen los objetivos generales del sistema y asignan el presupuesto y los recursos.
- **SDD Moderno — Fase de Constitución:** Esta etapa se formaliza mediante la creación del archivo de **Constitución** (`constitution.md` o directivas operativas en `AGENTS.md`). En estos artefactos se establecen los principios innegociables del proyecto, las restricciones arquitectónicas, el _stack_ tecnológico obligatorio, las convenciones de estilo de código y los límites de seguridad (_guardrails_) que gobernarán estrictamente tanto a los ingenieros humanos como a los agentes de IA.

---

### **Fase 2: Análisis de Requisitos ➔ Especificación Funcional (_Specify_)**

- **SDLC Clásico:** Los analistas de negocio y de requisitos interactúan con los clientes o usuarios finales para recopilar lo que el sistema debe hacer, plasmándolo en documentos de requisitos de producto (PRD), historias de usuario informales o extensas listas de requisitos funcionales y no funcionales.
- **SDD Moderno — Fase de Especificación:** Los requisitos del negocio se transforman en una **especificación técnica formal y estructurada** (como `spec.md` o `PRODUCT-SPEC.md`) escrita en Markdown. Para erradicar la ambigüedad que confunde a los modelos de lenguaje, se utiliza la notación sintáctica **EARS** (_Easy Approach to Requirements Syntax_) o contratos formales de API (OpenAPI/AsyncAPI). Esta especificación define con exactitud **qué** debe construir el sistema y **por qué**, abstrayéndose por completo de detalles de código fuente o infraestructura.

---

### **Fase 3: Diseño de Sistemas y Arquitectura ➔ Clarificación y Plan Técnico (_Clarify & Plan_)**

- **SDLC Clásico:** Los arquitectos de software diseñan la estructura técnica interna del sistema mediante diagramas de componentes, flujos de datos, modelos relacionales de bases de datos y especificaciones preliminares de interfaces.
- **SDD Moderno — Fase de Clarificación y Planificación Técnica:** Esta fase se divide en dos subprocesos complementarios:
  - **Clarificación (_Clarify_):** El equipo o un agente de IA audita activamente la especificación en busca de vacíos conceptuales, casos de borde no contemplados o contradicciones lógicas, realizando preguntas estructuradas para cerrar las decisiones de negocio antes de diseñar la solución técnica.
  - **Planificación Técnica (_Plan_):** Se genera el documento de diseño de ingeniería (`plan.md` o `TECHNICAL-SPEC.md`), que define la arquitectura de módulos, los esquemas de datos exactos (JSON Schema, SQL), las decisiones tecnológicas de dependencias y los contratos de integración (`INTEGRATION-SPEC.md`).

---

### **Fase 4: Desglose de Trabajo y Gestión de Backlog ➔ Descomposición en Tareas (_Tasks_)**

- **SDLC Clásico:** Los líderes técnicos y gestores de proyecto dividen el diseño en historias de usuario, épicas y tareas técnicas individuales (_tickets_ en Jira, Trello o GitHub Issues) asignadas manualmente a desarrolladores en tableros Scrum o Kanban.
- **SDD Moderno — Fase de Descomposición en Tareas:** El plan técnico se descompone de forma estructurada en una lista secuenciada de unidades de trabajo discretas, atómicas e independientes (`tasks.md`). Cada tarea se diseña específicamente para ser autocontenida y procesable en una sesión acotada de desarrollo dentro de la ventana de contexto de un agente de IA.

---

### **Fase 5: Implementación y Codificación ➔ Ejecución Agéntica Guiada (_Implement_)**

- **SDLC Clásico:** Los desarrolladores programan manualmente las líneas de código fuente en sus entornos integrados de desarrollo (IDEs) siguiendo las pautas de diseño establecidas.
- **SDD Moderno — Fase de Ejecución Agéntica:** La generación del código es asumida o acelerada por agentes de codificación con IA (como OpenCode, Claude Code, GitHub Copilot o Amazon Kiro) o desarrolladores asistidos. El agente toma tarea por tarea desde `tasks.md` y genera el código mínimo necesario junto con sus pruebas automatizadas, operando estrictamente restringido por el plan técnico y la constitución para evitar la alucinación de dependencias o patrones incompatibles.

---

### **Fase 6: Pruebas y Control de Calidad (QA) ➔ Validación de Contrato y Criterios (_Validate / Converge_)**

- **SDLC Clásico:** Los analistas de calidad (QA) ejecutan planes de prueba manuales y diseñan suites de pruebas automatizadas (unitarias, integración, regresión y de carga) sobre versiones empaquetadas para reportar defectos antes de la entrega.
- **SDD Moderno — Fase de Validación de Contrato:** Se implementa un doble mecanismo de verificación:
  - **Pruebas de Contrato Automatizadas (_Contract Testing_):** Se ejecutan linters de esquema y herramientas de prueba basadas en propiedades (como Schemathesis o Spectral) para garantizar que el software implementado coincida al 100% con los esquemas y contratos definidos.
  - **Bucle de Evaluación Agéntica y Humana (_Human-in-the-Loop_):** Se audita que todos los criterios de aceptación EARS y las métricas vinculadas a los IDs de la especificación se cumplan plenamente antes de autorizar la integración del código.

---

### **Fase 7: Despliegue y Mantenimiento ➔ Gobernanza Continua (_Spec-Anchored Evolution_)**

- **SDLC Clásico:** El software es desplegado en producción. Ante la aparición de fallos o nuevos requerimientos, los desarrolladores suelen realizar modificaciones urgentes directamente sobre el código fuente, provocando que la documentación técnica original quede desactualizada y se acumule deuda técnica con el tiempo.
- **SDD Moderno — Gobernanza Continua:** La especificación no muere tras el despliegue del software, sino que vive versionada en Git junto con la base de código bajo el modelo **Spec-Anchored**. Ante cualquier cambio o nueva funcionalidad, **se actualiza primero la especificación** y luego se regenera o refactoriza el código de forma alineada, eliminando por completo la divergencia de intención (_intent drift_) y manteniendo la coherencia arquitectónica a largo plazo.

---

## **2\. Tabla Comparativa: SDLC Clásico vs. SDD Moderno**

| Fase del SDLC               | SDLC Clásico (Tradicional)                    | SDD Moderno (Nativo de IA)                | Artefacto Clave en SDD                   |
| :-------------------------- | :-------------------------------------------- | :---------------------------------------- | :--------------------------------------- |
| **1\. Definición Inicial**  | Análisis de viabilidad y objetivos de negocio | **Constitución (_Setup_)**                | `constitution.md` / `AGENTS.md`          |
| **2\. Requisitos**          | Historias de usuario / Documentos PRD         | **Especificación (_Specify_)**            | `spec.md` / `PRODUCT-SPEC.md`            |
| **3\. Arquitectura/Diseño** | Diagramas UML y esquemas manuales             | **Clarificación y Plan Técnico (_Plan_)** | `plan.md` / `TECHNICAL-SPEC.md`          |
| **4\. Gestión de Tareas**   | Tableros Jira / Backlog manual                | **Descomposición en Tareas (_Tasks_)**    | `tasks.md`                               |
| **5\. Codificación**        | Programación manual por desarrolladores       | **Ejecución Agéntica (_Implement_)**      | Código fuente generado y verificado      |
| **6\. Control de Calidad**  | QA manual y pruebas unitarias posteriores     | **Validación de Contrato (_Validate_)**   | Test de contrato y revisión de criterios |
| **7\. Evolución**           | Mantenimiento sobre código (doc obsoleta)     | **Gobernanza Continua (_Spec-Anchored_)** | Especificación viva sincronizada en Git  |

---

## **3\. Beneficios Estratégicos de esta Transformación**

La transición del ciclo de vida tradicional al SDD proporciona tres ventajas competitivas fundamentales para los equipos de ingeniería:

1. **Eliminación del _Intent Drift_:** Asegura que el comportamiento final del sistema no se desvíe gradualmente de las necesidades reales del negocio a lo largo de las iteraciones.
2. **Control Determinista sobre la IA:** Proporciona un marco de contexto acotado y seguro (_guardrails_) que impide que los agentes de IA alucinen dependencias o inventen arquitecturas incompatibles.
3. **Paralelización Real del Trabajo:** Facilita que los equipos de interfaz (frontend) y servicios (backend) desarrollen en paralelo desde el primer día utilizando servidores simulados (_mock servers_) generados automáticamente a partir de los contratos de la especificación.

---
