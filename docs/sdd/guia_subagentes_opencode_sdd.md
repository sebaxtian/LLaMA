# **Guía Integral: Definición, Configuración e Integración de Subagentes en OpenCode y SDD**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

Un **Subagente** es un agente de Inteligencia Artificial especializado y subordinado que opera bajo la dirección de un agente primario o coordinador (_orchestrator_).

A diferencia de un agente primario que interactúa de manera directa y conversacional con el usuario, un subagente está diseñado para ejecutar **tareas atómicas, acotadas e independientes** en segundo plano o dentro de una subsesión aislada.

---

## **1\. ¿Qué es un Subagente?**

Un **Subagente** es una entidad de IA autónoma que cuenta con **su propia ventana de contexto y un conjunto de permisos estrictamente limitados**. Es invocado para resolver un problema puntual —como inspeccionar la base de código, redactar pruebas automatizadas, auditar arquitectura o implementar un módulo específico— y devolver sus conclusiones estructuradas al agente primario sin saturar la memoria ni la sesión de chat principal.

---

## **2\. Casos de Uso Principales**

- **Aislamiento de la Ventana de Contexto:** Evita consumir tokens de la sesión principal al escanear decenas de archivos, realizar búsquedas masivas o procesar dependencias extensas.
- **Principio de Menor Privilegio (Seguridad):** Permite restringir capacidades según el rol. Por ejemplo, es posible configurar un subagente de auditoría con permisos de **solo lectura** (_read-only_), impidiéndole modificar archivos de código o ejecutar comandos destructivos en la terminal.
- **Especialización de Roles de Ingeniería:** Facilita la división del trabajo en responsabilidades claras: un subagente arquitecto (`@planner`), un subagente programador (`@coder`), un subagente probador (`@tester`) y un subagente de revisión (`@reviewer`).
- **Ejecución Multiagente en Paralelo:** El agente coordinador puede instanciar de forma simultánea múltiples subagentes para analizar diferentes componentes del sistema o evaluar la especificación desde diversos ángulos concurrentemente.

---

## **3\. Principios de Definición y Ubicación en el Repositorio**

Los subagentes se definen de manera declarativa siguiendo los estándares de configuración del proyecto:

- **Ubicación en el Repositorio:**
  - `.opencode/agents/<nombre-subagente>.md` (específico del entorno **OpenCode**).
- **Formato de Archivo:** Documento Markdown compuesto por un encabezado de metadatos en **Frontmatter (YAML)** y directivas operativas en el cuerpo del texto.
- **Modo de Operación Declarado:** En el Frontmatter debe establecerse explícitamente el atributo `mode: subagent` para diferenciarlo de los agentes primarios interactivos.

---

## **4\. Elementos e Información Obligatoria del Subagente**

Para operar de forma determinista y segura, la definición de un subagente debe contener los siguientes componentes:

1. **Metadatos Frontmatter (YAML Obligatorio):**
   1. **`description`:** Explicación concisa de su función y del escenario exacto en el que debe ser invocado.
   2. **`mode`:** Debe configurarse estrictamente como `subagent`.
   3. **`permissions` / `tools`:** Matriz de permisos detallada (ej. `edit: false`, `bash: false` o lista de herramientas permitidas).
   4. **`model`:** El modelo a utilizar proveedor/modelo con un \#variante opcional. (ej. anthropic/claude-sonnet-5-5\#high)
2. **Directivas Procedimentales (System Prompt):**
   1. **Misión y Rol:** Declaración explícita del propósito del subagente.
   2. **Contexto de Entrada Obligatorio:** Lista de artefactos de gobernanza que debe consultar antes de actuar (ej. `@docs/constitution.md`, `@spec.md`, `@plan.md`).
   3. **Instrucciones Paso a Paso:** Procedimiento secuencial para completar la tarea.
   4. **Prohibiciones y Guardrails:** Límites expresos de lo que NO tiene autorización de modificar o asumir.
   5. **Formato de Salida:** Estructura de reporte esperada para comunicar los resultados al agente primario.
3. **Identificador único del subagente:** Está determinado por el nombre del archivo en `.opencode/agents/<nombre-subagente>.md` (ej. `reviewer.md`, `planner.md`, `tester.md,coder.md`).

---

## **5\. Función de los Subagentes en la Metodología SDD (_Spec-Driven Development_) pura**

Dentro del flujo de **Desarrollo Basado en Especificaciones (SDD)**, los subagentes ejecutan las fases de la metodología garantizando la modularidad y evitando la contaminación de contexto:

```
                     ┌────────────────────────────────┐
                     │   AGENTE COORDINADOR / PRIMARY │
                     └───────────────┬────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          ▼                          ▼                          ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ @planner         │       │ @coder           │       │ @reviewer        │
│ Subagente        │       │ Subagente        │       │ Subagente        │
│ Redacta plan.md  │       │ Ejecuta TDD      │       │ Audita contrato  │
│ y tasks.md       │       │ en Build Mode    │       │ y constitution   │
└──────────────────┘       └──────────────────┘       └──────────────────┘
 (Fases 2, 3, 4, 5)            (Fase 6)                    (Fase 7)
```

- **Prevención del Sesgo de Confirmación:** Impide que el mismo modelo que generó el código audite sus propias fallas; un subagente `@reviewer` independiente evalúa la solución con una perspectiva neutral y objetiva.
- **Modularidad del Pipeline:** Cada subagente se especializa en un artefacto concreto del ciclo de vida SDD (`spec.md`, `plan.md`, `tasks.md` o `validation_report.md`).

---

## **6\. ¿En qué Etapa del Flujo SDD debe ser Creado?**

La definición de los subagentes debe realizarse en la **Etapa 1: Constitución y Setup del Proyecto**.

Junto con la redacción de `constitution.md`, la configuración de `AGENTS.md`, la instalación de habilidades (_skills_) y la vinculación de servidores MCP, se crean los archivos de subagentes en la carpeta `.opencode/agents/`. A partir de ese momento, los subagentes son **invocados dinámicamente a lo largo de las Etapas 2 a 7** del ciclo SDD.

---

## **7\. Integración Operacional con OpenCode**

**OpenCode** gestiona subagentes de manera nativa mediante las siguientes capacidades:

- **Subagentes Integrados de Fábrica:** Incluye por defecto herramientas como `@explore` (subagente de solo lectura optimizado para indexar y buscar código) y `@general` (diseñado para investigaciones de múltiples pasos).
- **Invocación Explícita mediante `@`:** El usuario puede llamar a cualquier subagente directamente en el chat anteponiendo una arroba:

```
@reviewer Audita los cambios en git diff contra @docs/constitution.md
```

- **Orquestación Autónoma por Agentes Primarios:** Al solicitar a un agente primario (como `build`, `plan` o un agente coordinador personalizado) que ejecute un flujo SDD, este delega tareas, transmite contexto y consolida las respuestas de los subagentes en segundo plano.
- **Inspección Visual en la TUI:** Cuando un subagente entra en ejecución, la interfaz de terminal de OpenCode muestra un hilo en segundo plano que puede inspeccionarse presionando la tecla de flecha hacia abajo (`↓`).

---

## **8\. Plantilla Optimizada y Estandarizada (`.opencode/agents/subagente.md`)**

```
# subagente.md (Ejemplo base)

---
description: [Descripción concisa del rol y cuándo debe ser invocado por el coordinador]
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: deny
---

# Subagente: [Nombre del Subagente]

## 1. Misión y Rol
Eres el **Subagente [Rol]**. Tu objetivo exclusivo es [definición clara de la tarea].

## 2. Contexto de Entrada Obligatorio
Antes de actuar, lee y analiza obligatoriamente:
- **Constitución:** `@docs/constitution.md`
- **Especificación Activa:** `@specs/[feature]/spec.md`

## 3. Procedimiento de Ejecución
1. **Paso 1:** Inspecciona los archivos de origen en `src/` o `tests/`.
2. **Paso 2:** Analiza la conformidad con las reglas establecidas.
3. **Paso 3:** Elabora el reporte de hallazgos.

## 4. Restricciones y Guardrails
- NO modifiques ningún archivo de código fuente.
- NO asumas reglas de negocio no escritas en la especificación.

## 5. Formato de Salida
Reporta tus resultados en una lista estructurada con los siguientes campos:
- **Estado:** [Aprobado / Rechazado]
- **Observaciones:** [Lista de hallazgos]
```

---

## **9\. Ejemplo Práctico: Subagente Revisor (`.opencode/agents/reviewer.md`)**

A continuación se presenta la configuración real de un **subagente** de revisión diseñado para auditar código en **OpenCode** bajo el marco SDD:

```
# reviewer.md (Ejemplo base)

---
description: Subagente de solo lectura para auditar código y verificar que cumpla al 100% con la especificación y la constitución.
mode: subagent
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: allow
---

# Subagente: Revisor de Calidad y Contrato (`reviewer`)

## 1. Misión y Rol
Eres el **Subagente Revisor (Reviewer)**. Tu función es auditar el código generado por la etapa de implementación sin modificarlo, garantizando que cumpla con los principios de la constitución y los criterios de aceptación EARS.

## 2. Contexto de Entrada
Antes de emitir tu dictamen, debes leer:
- `@docs/constitution.md`
- `@specs/NNN-slug/spec.md`
- `@specs/NNN-slug/plan.md`

## 3. Pasos de Auditoría
1. Revisa los cambios recientes en el código (`git diff` o archivos en `src/`).
2. Verifica que las pruebas automatizadas en `tests/` cubran todos los requisitos `RF-xxx` descritos en `spec.md`.
3. Ejecuta la suite de pruebas mediante el comando `pytest` y confirma que el 100% de los tests pasen.
4. Confirma que el código respete el tipado estricto (`mypy`) y no instale dependencias no autorizadas.

## 4. Restricciones
- Tienes totalmente prohibido editar archivos en `src/` o `tests/`.
- Tu respuesta debe ser un reporte cuantitativo y objetivo.

## 5. Formato de Respuesta
### Reporte de Auditoría de Calidad
- **Cumplimiento de Especificación:** [100% / Incompleto]
- **Pruebas Automatizadas:** [Pasadas / Falladas]
- **Dictamen Final:** [CONVERGIDO / DIVERGENTE]
- **Brechas Encontradas:** [Lista de brechas o 'Ninguna']
```

---
