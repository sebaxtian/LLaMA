# **Guía Integral: Definición, Notación EARS y Gobernanza Funcional de `spec.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El archivo **`spec.md`** (o `PRODUCT-SPEC.md` / `requirements.md`) representa la **especificación funcional y de negocio** de una característica o incremento de software específico dentro de la metodología de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**.

Mientras que la Constitución del repositorio (`constitution.md`) establece las normas innegociables del proyecto y el plan técnico (`plan.md`) define el diseño de ingeniería, **`spec.md`** se enfoca exclusivamente en capturar con precisión la **intención del producto**: define el **QUÉ** debe construir el sistema y el **POR QUÉ**, aislando completamente la lógica de negocio de los detalles de código o infraestructura.

---

## **1\. ¿Qué es `spec.md`?**

**`spec.md`** es el documento que formaliza, estructura y hace legible —tanto para humanos como para agentes de Inteligencia Artificial— la **intención de negocio de una funcionalidad**.

A diferencia de los documentos de requisitos funcionales tradicionales (PRD en Word o wikis aisladas) que suelen quedar desactualizados y olvidados tras la fase de análisis, en SDD `spec.md` se versiona en Git junto con la base de código y actúa como un **contrato vivo**. Este contrato guía directamente la generación automatizada de pruebas, la arquitectura técnica y el comportamiento determinista de los agentes de codificación (como **OpenCode**, Claude Code o GitHub Spec Kit).

---

## **2\. Casos de Uso Principales**

- **Definir la intención antes de codificar:** Erradica el desarrollo impulsado por _prompts_ informales e improvisados (_vibe coding_), obligando al equipo a cerrar las decisiones de producto antes de generar código fuente.
- **Servir como contrato vinculante entre humanos e IA:** Ofrece límites estrictos (_guardrails_) para que el agente de codificación implemente con exactitud la lógica esperada, evitando alucinaciones, omisiones o la invención de reglas de negocio.
- **Eliminar la divergencia de intención (_Intent Drift_):** Asegura que el comportamiento final del sistema no se desvíe progresivamente de las necesidades originales del usuario a lo largo de sucesivas iteraciones o refactorizaciones.
- **Generar pruebas automatizadas y criterios de aceptación:** Gracias al uso de notaciones formales como **EARS** (_Easy Approach to Requirements Syntax_), cada requisito de `spec.md` se mapea de forma directa e inequívoca a un caso de prueba ejecutable.

---

## **3\. Principios de Definición y Aislamiento Técnico**

- **Ubicación en el Repositorio:** Se organiza dentro de una carpeta dedicada a la característica (feature) en `specs/` (por ejemplo, `specs/001-user-auth/spec.md` o `specs/002-csv-export/spec.md`).
- **Aislamiento Técnico Estricto:** `spec.md` describe comportamiento funcional observable y reglas de negocio puras. **No debe contener** rutas de archivos de código, nombres de clases o métodos, esquemas SQL, nombres de frameworks ni comandos de terminal; todos esos aspectos pertenecen a la etapa de planificación técnica (`plan.md`).
- **Sintaxis EARS para Requisitos:** Para eliminar la ambigüedad inherente al lenguaje natural, los requisitos funcionales se redactan utilizando los **5 patrones sintácticos de EARS** deterministas:
  - **Ubicuo (Comportamiento continuo/siempre activo):**  
    &nbsp;`El <sistema> debe <respuesta>`.
  - **Dirigido por Eventos (Desencadenado por una acción):**  
    &nbsp;`Cuando <evento desencadenante>, el <sistema> debe <respuesta>`.
  - **Dirigido por Estados (Activo mientras se cumple una condición):**  
    &nbsp;`Mientras <estado>, el <sistema> debe <respuesta>`.
  - **Característica Opcional (Comportamiento condicionado a una opción del sistema):**  
    &nbsp;`Donde <característica opcional>, el <sistema> debe <respuesta>`.
  - **Comportamiento No Deseado / Excepción (Manejo de errores o fallos):**  
    &nbsp;`Si <error o condición no deseada>, entonces el <sistema> debe <respuesta>`.

---

## **4\. Elementos e Información Obligatoria que debe Contener**

1. **Contexto y Objetivo de Negocio:** Explicación concisa del problema que resuelve la característica y el valor aportado al usuario.
2. **Actores y Roles de Usuario:** Definición de quiénes interactúan con la funcionalidad y sus niveles o permisos de acceso.
3. **Requisitos Funcionales (Notación EARS \+ IDs únicos):** Lista numerada de requisitos verificables (`RF-001`, `RF-002`, etc.) redactados con las fórmulas sintácticas de EARS.
4. **Casos Borde y Manejo de Excepciones (`CB-xxx`):** Definición explícita de cómo debe reaccionar el sistema ante datos inválidos, límites numéricos o fallos de entrada.
5. **Fuera de Alcance (_Out of Scope_):** Declaración explícita de lo que **NO** se construirá en la iteración actual para prevenir la sobreingeniería (_scope creep_).
6. **Criterios de Aceptación (_Definition of Done_):** Lista de condiciones verificables necesarias para considerar aprobada la especificación.

---

## **5\. Rol en la Metodología SDD y Etapa en el Flujo**

En el ciclo de vida de **7 etapas del SDD puro**, la especificación corresponde a la **Etapa 2: Especificar (_Specify_)**:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • docs/constitution.md (Leyes fundamentales del repositorio)           │
 │  • AGENTS.md (Límites operativos del entorno y System Prompt)           │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 2: ESPECIFICACIÓN (Specify)                                  │
 │  • specs/NNN-slug/spec.md (Requisitos de negocio en notación EARS determinista)     │
 │  • Se crea aquí: Define el QUÉ y el POR QUÉ                                          │
 └────────────────────────────────────┬─────────────────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                    ETAPA 3: CLARIFICACIÓN (Clarify)                     │
 │  • specs/NNN-slug/clarify.md (Auditoría QA y resolución de vacíos)     │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                  ETAPA 4: PLANIFICACIÓN TÉCNICA (Plan)                  │
 │  • specs/NNN-slug/plan.md (Diseño técnico, arquitectura y esquemas)    │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 5: TAREAS ATÓMICAS (Tasks)                      │
 │  • specs/NNN-slug/tasks.md (Desglose ejecutable en checkboxes)         │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 6: IMPLEMENTACIÓN (Implement)                   │
 │  • Bucle TDD (Red -> Green -> Refactor) por cada tarea                  │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 7: VALIDACIÓN (Validate)                      │
 │  • specs/NNN-slug/validation_report.md (Auditoría contra la spec)      │
 └─────────────────────────────────────────────────────────────────────────┘
```

- **Función Clave:** Tras definirse las leyes base del repositorio en la Etapa 1 (constitution.md y AGENTS.md), la redacción de spec.md en la Etapa 2 actúa como el disparador obligatorio de cualquier incremento o funcionalidad en el proyecto.

---

## **6\. Integración Operacional con OpenCode**

**OpenCode** cuenta con mecanismos nativos para interpretar, generar y verificar `spec.md`:

- **Lectura Automática de Convenciones:** Al iniciar sesión, OpenCode examina `AGENTS.md`, donde se declara la convención de especificaciones del proyecto (por ejemplo: _"Consultar la especificación activa en `specs/NNN-slug/spec.md` antes de implementar"_), alineando las respuestas del modelo al estándar establecido.
- **Aislamiento de Contexto mediante `@`:** Durante la interacción en la terminal (TUI) de OpenCode, se puede invocar `@specs/NNN-slug/spec.md` para inyectar exclusivamente el contexto funcional relevante sin saturar la memoria con código innecesario.
- **Comandos Slash y Habilidades (_Skills_):** Es común definir comandos slash como `/spec` o `/specify` (o habilidades en `.opencode/skills/`) para que **OpenCode** interactúe como un Product Owner técnico, formulando preguntas para estructurar los requisitos en notación EARS antes de avanzar a la etapa técnica.

---

## **7\. Plantilla Optimizada y Estandarizada (`spec.md`)**

```
# spec.md (Ejemplo base)

# Especificación: [Nombre de la Funcionalidad / Módulo]

## 1. Contexto y Objetivo
[Descripción breve del problema de negocio que se resuelve y el valor que aporta al usuario final o sistema consumidor].

## 2. Actores y Permisos
- **[Nombre del Rol 1]:** [Descripción de permisos, capacidades y nivel de acceso].
- **[Nombre del Rol 2]:** [Descripción de permisos, capacidades y nivel de acceso].

## 3. Requisitos Funcionales (Notación EARS)
- **RF-001 (Ubicuo):** El [Nombre del Sistema] debe [comportamiento siempre activo].
- **RF-002 (Evento):** Cuando [evento desencadenante o acción del usuario], el [Nombre del Sistema] debe [respuesta esperada del sistema].
- **RF-003 (Estado):** Mientras [condición o estado operativo activo], el [Nombre del Sistema] debe [respuesta esperada del sistema].
- **RF-004 (Opción):** Donde [característica u opción opcional presente], el [Nombre del Sistema] debe [respuesta esperada del sistema].
- **RF-005 (Error/Excepción):** Si [condición no deseada, fallo o error de entrada], entonces el [Nombre del Sistema] debe [respuesta esperada del sistema].

## 4. Casos Borde y Manejo de Excepciones
- **CB-001:** [Escenario límite de entrada de datos, volúmenes atípicos o combinaciones inusuales].
- **CB-002:** [Comportamiento esperado ante fallos de persistencia, concurrencia o tiempos de espera].

## 5. Fuera de Alcance (Out of Scope)
- [Funcionalidad, formato o integración que explícitamente NO se implementará en esta iteración].

## 6. Criterios de Aceptación (Definition of Done)
- [ ] Todos los requisitos funcionales (RF-001 a RF-005) cuentan con pruebas automatizadas asociadas.
- [ ] Se verifica mediante pruebas automatizadas que los casos borde (CB-001 y CB-002) se manejan adecuadamente.
- [ ] La especificación no entra en contradicción con `docs/constitution.md`.
```

---

## **8\. Ejemplo Práctico: Especificación para "Exportación de Tareas a CSV"**

A continuación se muestra un ejemplo real del archivo `specs/NNN-slug/spec.md` formulado para un sistema de seguimiento de tareas en consola:

```
# spec.md (Ejemplo base)

# Especificación: Exportación de Tareas a CSV

## 1. Contexto y Objetivo
Permitir a los administradores del sistema descargar un informe en formato CSV con el listado de tareas registradas para realizar auditorías externas de productividad y respaldos de datos.

## 2. Actores y Permisos
- **Administrador:** Usuario con permisos totales para solicitar y descargar el archivo CSV.
- **Usuario Estándar:** Usuario regular que NO debe tener acceso a la función de exportación.

## 3. Requisitos Funcionales (Notación EARS)
- **RF-001 (Evento):** Cuando el Administrador ejecute la solicitud de exportación en formato CSV, el TaskTracker debe generar un archivo codificado en UTF-8 que contenga la lista de tareas filtradas.
- **RF-002 (Ubicuo):** El TaskTracker debe incluir una fila de encabezado con los campos exactos: `id, titulo, estado, fecha_creacion`.
- **RF-003 (Excepción):** Si la consulta de tareas no devuelve ningún registro, entonces el TaskTracker debe generar un archivo CSV que contenga únicamente la fila de encabezado sin arrojar errores.
- **RF-004 (Excepción):** Si un Usuario Estándar intenta solicitar la exportación, entonces el TaskTracker debe denegar la acción y mostrar el mensaje "Acceso denegado: requiere rol de Administrador".

## 4. Casos Borde y Manejo de Excepciones
- **CB-001 (Caracteres Especiales):** Si el título de una tarea contiene comas, saltos de línea o comillas dobles, el TaskTracker debe envolver el campo entre comillas dobles siguiendo el estándar RFC 4180.
- **CB-002 (Inyección CSV):** Si el título de una tarea comienza con los caracteres `=`, `+`, `-` o `@`, el TaskTracker debe escapar dicho carácter inicial anteponiendo un apóstrofe para evitar la ejecución de fórmulas en hojas de cálculo.

## 5. Fuera de Alcance (Out of Scope)
- Exportación en formatos PDF o Excel (.xlsx).
- Envío automático del archivo CSV generado por correo electrónico.

## 6. Criterios de Aceptación (Definition of Done)
- [ ] El archivo generado cumple estrictamente con el formato RFC 4180.
- [ ] Se verifica mediante pruebas unitarias que los usuarios estándar reciben una respuesta de rechazo explícita ante el intento de exportación.
- [ ] La totalidad de requisitos funcionales (RF-001 a RF-004) y casos borde están cubiertos por pruebas automatizadas.
```

---
