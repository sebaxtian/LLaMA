# **Guía Integral: Definición, Descomposición Operativa y Secuenciación de `tasks.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El archivo **`tasks.md`** (o plan de ejecución de tareas) representa la **fase de descomposición operativa y secuenciación de trabajo** dentro de la metodología de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**.

Mientras que `spec.md` define el **QUÉ** de negocio y `plan.md` establece el **CÓMO** técnico y de arquitectura, `tasks.md` descompone esa arquitectura en una lista estructurada de **unidades de trabajo discretas, atómicas, independientes y secuenciadas** deterministas.

---

## **1\. ¿Qué es `tasks.md`?**

**`tasks.md`** es el documento ejecutable que transforma el diseño técnico en un conjunto de instrucciones pequeñas con casillas de verificación (_checkboxes_) diseñadas específicamente para ser procesadas en **sesiones acotadas de desarrollo**.

En el SDD nativo de Inteligencia Artificial, `tasks.md` actúa como la **interfaz de ejecución entre el desarrollador y el agente de codificación**. Cada tarea está calculada para ejecutarse dentro de la ventana de contexto de un modelo de lenguaje (o en bloques cortos de 15 a 30 minutos por un programador humano), evitando que la IA pierda la atención o intente modificar demasiados archivos al mismo tiempo.

---

## **2\. Casos de Uso Principales**

- **Principio de "Divide y Vencerás":** Evita emitir al agente de IA la orden masiva de _"construye toda la funcionalidad de una vez"_, práctica que suele derivar en código incompleto, fallos de sintaxis o alucinaciones de librerías.
- **Control de la Ventana de Contexto:** Garantiza que el modelo trabaje con el foco acotado en un único problema bien delimitado, reduciendo el consumo innecesario de tokens y los errores conceptuales.
- **Desarrollo Guiado por Pruebas (TDD Estricto):** Permite estructurar el desarrollo bajo un ciclo disciplinado: escribir las pruebas unitarias asociadas a la tarea, verificar que fallen (rojo), implementar el código mínimo indispensable y confirmar que pasen (verde).
- **Seguimiento Visual y Estado de Progreso:** Al utilizar el formato estándar de casillas en Markdown (`- [ ]` y `- [x]`), tanto el desarrollador como el agente pueden inspeccionar el estado actual del proyecto en todo momento.
- **Trazabilidad Directa con Requisitos:** Cada tarea se vincula explícitamente a los identificadores de requisitos funcionales (`RF-xxx`) de la especificación original, asegurando que no se escriba código sobrante ni se omita ningún criterio de aceptación.

---

## **3\. Principios de Definición y Ubicación en el Repositorio**

- **Ubicación en el Repositorio:** Se almacena dentro de la carpeta asignada a la característica en `specs/` (por ejemplo, `specs/NNN-slug/tasks.md` o `specs/002-auth-login/tasks.md`).
- **Formato Estándar:** Documento Markdown interactivo con casillas de verificación navegables.
- **Dependencias Explícitas:** Cada tarea debe declarar si depende de la finalización de un paso previo o si puede ejecutarse de forma aislada.

---

## **4\. Elementos e Información Obligatoria que debe Contener**

Para garantizar una ejecución determinista, cada bloque dentro de `tasks.md` debe incluir:

1. **Identificador y Título de la Tarea:** Nombre claro y numerado de la unidad de trabajo (ej. _Tarea 1: Estructura base de persistencia_).
2. **Dependencias Directas (_Depends on_):** Declaración de si la tarea requiere la finalización previa de otra unidad (ej. _Depende de: Tarea 1_).
3. **Requisitos Cubiertos (`RF-xxx` / `CB-xxx`):** IDs exactos de los requisitos funcionales o casos de borde de `spec.md` que satisface esta tarea.
4. **Descripción del Trabajo:** Explicación técnica concisa de los archivos que se deben crear o modificar y las funciones a implementar.
5. **Criterios de Aceptación (Verificación):** Casillas con afirmaciones comprobables que determinan si la tarea está completada (ej. `- [ ] El test test_export_header pasa con éxito`).
6. **Matriz de Paralelización (Opcional):** Tabla que indica qué tareas son independientes entre sí para ser delegadas a agentes secundarios en paralelo.

---

## **5\. Función en la Metodología SDD y Etapa en el Flujo**

Dentro del ciclo de vida de **7 etapas del SDD puro**, la descomposición de tareas corresponde a la **Etapa 5: Tareas (_Tasks_)**:

```
[Etapa 1: Constitution & AGENTS.md]  ──► Leyes y límites generales del proyecto
              │
              ▼
[Etapa 2: Specify (spec.md)]         ──► Requisitos funcionales de negocio (QUÉ)
              │
              ▼
[Etapa 3: Clarify (clarify.md)]      ──► Inspección QA, vacíos y ambigüedades
              │
              ▼
[Etapa 4: Plan (plan.md)]            ──► Diseño técnico y arquitectura (CÓMO)
              │
              ▼
[Etapa 5: Tasks (tasks.md)]           ──► Desglose en tareas atómicas ejecutables (Fase Actual)
              │
              ▼
[Etapa 6: Implement]                  ──► Codificación guiada por tareas + TDD
              │
              ▼
[Etapa 7: Validate]                   ──► Verificación de contrato contra la spec
```

- **Función Clave:** Servir de mapa de ruta directo para la **Etapa 6 (Implementación)**. En lugar de implementar contra todo el documento de arquitectura de forma desordenada, el agente toma secuencialmente las tareas de `tasks.md`, escribe las pruebas, genera el código y marca la casilla como completada (`- [x]`).

---

## **6\. Integración Operacional con OpenCode**

**OpenCode** cuenta con soporte agéntico nativo para la creación, lectura y actualización de `tasks.md`:

- **Comandos Slash Nativos (`/tasks` e `/implement`):**
  - Al ejecutar `/tasks` (o el comando correspondiente en `.opencode/commands/tasks.md`), OpenCode lee `@spec.md` y `@plan.md` para generar automáticamente el desglose de `tasks.md` sin tocar el código fuente todavía.
  - Al ejecutar `/implement`, OpenCode lee `tasks.md`, identifica la primera casilla no marcada (`- [ ]`), la resuelve en TDD, ejecuta las pruebas y cambia la casilla a marcada (`- [x]`) de forma autónoma.
- **Aislamiento por Referencia `@`:** Para evitar saturar la memoria de **OpenCode**, se inyecta la tarea específica directamente en el chat con la instrucción: _"Implementa únicamente la Tarea 2 descrita en `@specs/NNN-slug/tasks.md` y detente al terminar"_.
- **Orquestación Multiagente (_Coordinator / Subagentes_):** En arquitecturas multiagente (como **OpenCode** con subagentes `@planner`, `@coder` y `@reviewer`), el agente coordinador utiliza `tasks.md` como el tablero Kanban central para repartir trabajo a los subagentes en segundo plano y monitorear el avance del proyecto.

---

## **7\. Plantilla Optimizada y Estandarizada (`tasks.md`)**

```
# tasks.md (Ejemplo base)

# Plan de Ejecución de Tareas: [Nombre de la Funcionalidad]

## Referencias
- **Especificación Funcional:** `specs/[id-feature]/spec.md`
- **Plan Técnico:** `specs/[id-feature]/plan.md`

---

## Tarea 1: [Nombre de la Tarea Inicial]
**Depende de:** Ninguna (Tarea inicial)
**Requisitos cubiertos:** RF-001

**Descripción:**
[Descripción técnica clara del archivo a crear y la interfaz base].

**Criterios de Aceptación:**
- [ ] La estructura de archivos `src/...` existe y los tipos compilan.
- [ ] La prueba unitaria de inicialización en `tests/...` se ejecuta correctamente.

---

## Tarea 2: [Nombre de la Segunda Tarea]
**Depende de:** Tarea 1
**Requisitos cubiertos:** RF-002, CB-001

**Descripción:**
[Descripción de la lógica de negocio y manejo de errores].

**Criterios de Aceptación:**
- [ ] Implementar la función/método `[nombre_metodo]()`.
- [ ] Verificar que la prueba unitaria `test_[escenario]` pase en la suite de pruebas.

---

## Tarea 3: Integración y Verificación Final
**Depende de:** Tarea 1, Tarea 2
**Requisitos cubiertos:** RF-003, RF-004

**Descripción:**
[Conectar el módulo con la interfaz CLI/API y validar la ejecución completa].

**Criterios de Aceptación:**
- [ ] La interfaz de usuario / consola responde según el contrato especificado.
- [ ] El 100% de la suite de pruebas automatizadas pasa sin errores.

---

## Matriz de Paralelización (Opcional)
| Grupo | Tareas Independientes | Requisito Previo |
| :--- | :--- | :--- |
| Core / Dominio | Tarea 1 -> Tarea 2 | Ninguno |
| UI / Consola | Tarea 3 | Tarea 2 finalizada |
```

---

## **8\. Ejemplo Práctico: Desglose para "Exportación de Tareas a CSV"**

A continuación se muestra un ejemplo real del archivo `specs/NNN-slug/tasks.md` coherente con el módulo desarrollado en las guías previas:

```
# tasks.md (Ejemplo base)

# Plan de Ejecución de Tareas: Exportación de Tareas a CSV

## Referencias
- **Especificación Funcional:** `specs/NNN-slug/spec.md`
- **Plan Técnico:** `specs/NNN-slug/plan.md`

---

## Tarea 1: Pruebas y Sanitización de Inyección CSV (Core Exporter)
**Depende de:** Ninguna
**Requisitos cubiertos:** RF-001, CB-001

**Descripción:**
Crear el módulo `src/core/exporter.py` e implementar el método estático `CSVTaskExporter.sanitize_field()`. Escribir primero las pruebas unitarias para asegurar que los títulos de tareas que inicien con `=`, `+`, `-` o `@` sean escapados con un apóstrofe `'`.

**Criterios de Aceptación:**
- [ ] Test `test_sanitize_normal_string`: Retorna la cadena sin modificaciones.
- [ ] Test `test_sanitize_formula_injection`: `=SUM(A1:A10)` se convierte en `'=SUM(A1:A10)`.
- [ ] La suite `pytest tests/test_csv_exporter.py` pasa con 100% de éxito.

---

## Tarea 2: Generación del Contenido CSV y Encabezados RFC 4180
**Depende de:** Tarea 1
**Requisitos cubiertos:** RF-002, RF-003

**Descripción:**
Implementar `CSVTaskExporter.generate_csv_content(tasks: list[Task]) -> str`. Garantizar que siempre se emita la fila de encabezado `id,titulo,estado,fecha_creacion` aun cuando la lista de tareas esté vacía.

**Criterios de Aceptación:**
- [ ] Test `test_empty_task_list_returns_header_only`: Retorna exactamente la fila de encabezado.
- [ ] Test `test_valid_tasks_formatting`: Formatea correctamente fechas ISO 8601 y strings con comas según RFC 4180.
- [ ] Pruebas unitarias ejecutadas e integradas.

---

## Tarea 3: Comando CLI y Verificación de Permisos
**Depende de:** Tarea 2
**Requisitos cubiertos:** RF-004

**Descripción:**
Integrar el comando `export-csv` en `src/cli/commands.py`. Verificar el rol del usuario activo; si no es `Administrador`, abortar la ejecución mostrando "Acceso denegado: requiere rol de Administrador".

**Criterios de Aceptación:**
- [ ] Test `test_unauthorized_user_blocked`: Un usuario estándar recibe error de permiso.
- [ ] Test `test_admin_export_success`: Un usuario administrador genera y guarda el archivo CSV.
- [ ] Verificación de linter (`ruff`) y comprobación de tipos (`mypy`) superadas.
```

---
