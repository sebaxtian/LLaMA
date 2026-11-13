# **Guía de Referencia: Las 7 Etapas del Ciclo de Vida del Desarrollo Basado en Especificaciones (SDD Puro)**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)** puro es una metodología de ingeniería de software donde una especificación formal, estructurada y legible por máquina actúa como la **única fuente de verdad** del sistema. En el SDD puro (independiente de herramientas o _frameworks_ específicos como Spec Kit, OpenSpec o Kiro), el desarrollo sigue un ciclo de vida riguroso de **7 etapas secuenciales** donde se separa estrictamente el **QUÉ** se construye del **CÓMO** se implementa.

---

## **1\. Flujo General del Ciclo de Vida (Visión Global)**

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • docs/constitution.md (Reglas innegociables, stack y guardrails)      │
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
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                    ETAPA 3: CLARIFICACIÓN (Clarify)                     │
 │  • specs/NNN-slug/clarify.md (Inspección QA de ambigüedades y vacíos)  │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                  ETAPA 4: PLANIFICACIÓN TÉCNICA (Plan)                  │
 │  • specs/NNN-slug/plan.md (Arquitectura, contratos API y esquemas)     │
 │  • Define el CÓMO técnico formal                                        │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 5: TAREAS ATÓMICAS (Tasks)                      │
 │  • specs/NNN-slug/tasks.md (Desglose en unidades ejecutables acotadas) │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 6: IMPLEMENTACIÓN (Implement)                   │
 │  • Bucle TDD (Red -> Green -> Refactor) ejecutado tarea por tarea       │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 7: VALIDACIÓN (Validate)                      │
 │  • specs/NNN-slug/validation_report.md (Pruebas de contrato y cierre)  │
 └─────────────────────────────────────────────────────────────────────────┘
```

---

## **2\. Desglose Operativo Etapa por Etapa**

### **Etapa 1: Constitución del Proyecto (`constitution.md`)**

#### **Propósito y Concepto**

Establece los principios arquitectónicos innegociables, estándares de código, políticas de pruebas, stack tecnológico obligatorio y límites de seguridad (_guardrails_) del proyecto. Funciona como el marco normativo que rige a desarrolladores y agentes de Inteligencia Artificial durante todo el ciclo de vida. Se crea una sola vez al inicio del proyecto.

#### **Plantilla (`docs/constitution.md`)**

```
# Constitución del Proyecto: [Nombre del Proyecto]

## 1. Principios Innegociables
- **Principio 1:** La especificación es la única fuente de verdad; ningún código se escribe sin spec.
- **Principio 2:** Separación estricta entre la lógica de negocio y la interfaz/adaptadores.
- **Principio 3:** Cobertura de pruebas automatizadas obligatoria para cada requisito funcional.

## 2. Stack Tecnológico y Restricciones
- **Lenguaje/Runtime:** [ej. Python 3.12 / TypeScript 5.x]
- **Persistencia:** [ej. PostgreSQL / Archivos JSON locales]
- **Frameworks autorizados:** [Lista explícita de librerías permitidas]

## 3. Normas de Calidad y Testing
- TDD obligatorio (Escribir prueba reducida antes de la implementación).
- Notación EARS para todos los requisitos funcionales.
```

#### **Ejemplo Práctico (TaskTracker CLI)**

```
# Constitución del Proyecto: TaskTracker CLI

## 1. Principios Innegociables
- Toda modificación requiere actualizar primero el archivo de especificación correspondiente.
- El núcleo de dominio no debe depender de ninguna librería externa de I/O o CLI.
- Ninguna función pública puede carecer de prueba unitaria asociada.

## 2. Stack Tecnológico
- Lenguaje: Python 3.12 (typing estricto con mypy).
- Almacenamiento: Archivo local JSON aislado.
```

---

### **Etapa 2: Especificación Funcional (`spec.md`)**

#### **Propósito y Concepto**

Documenta el comportamiento esperado del sistema, los roles de usuario y las historias de usuario mediante la notación sintáctica **EARS** (_Easy Approach to Requirements Syntax_).

> **Regla de oro:** Se describe exclusivamente el **QUÉ** debe hacer el sistema y el **POR QUÉ**, sin incluir detalles técnicos de implementación o código.

Los 5 patrones sintácticos de EARS aplicados aquí son:

- **Ubicuo:** `El <sistema> debe <respuesta>` (siempre activo).
- **Dirigido por Eventos:** `Cuando <evento>, el <sistema> debe <respuesta>`.
- **Dirigido por Estados:** `Mientras <estado>, el <sistema> debe <respuesta>`.
- **Opción Opcional:** `Donde <opción>, el <sistema> debe <respuesta>`.
- **Comportamiento No Deseado:** `Si <error/excepción>, entonces el <sistema> debe <respuesta>`.

#### **Plantilla (`specs/NNN-slug/spec.md`)**

```
# Especificación: [Nombre de la Funcionalidad / MVP]

## Contexto y Objetivo
[Descripción clara del problema de negocio que se resuelve]

## Actores y Roles
- **[Nombre de Rol]:** [Descripción de permisos y objetivos]

## Requisitos Funcionales (Sintaxis EARS)
- **RF-001 (Ubicuo):** El [Sistema] debe [Respuesta].
- **RF-002 (Evento):** Cuando [Evento], el [Sistema] debe [Respuesta].
- **RF-003 (Excepción):** Si [Condición de Error], entonces el [Sistema] debe [Respuesta].

## Casos Límite y Fueras de Alcance
- **Casos Borde:** [Lista de situaciones extremas]
- **Fuera de Alcance:** [Lo que explícitamente NO se construirá en esta iteración]
```

#### **Ejemplo Práctico (`specs/NNN-slug/spec.md`)**

```
# Especificación: Creación de Tareas MVP

## Requisitos Funcionales (EARS)
- **RF-001:** Cuando el usuario ejecute el comando de creación con un título válido, el TaskTracker CLI debe almacenar la tarea con estado 'pendiente' y generar un UUID único.
- **RF-002:** Si el título introducido está vacío o contiene solo espacios, entonces el TaskTracker CLI debe mostrar un mensaje de error "El título no puede estar vacío" y abortar sin guardar.
- **RF-003:** Mientras existan tareas registradas, el TaskTracker CLI debe listar las tareas ordenadas por fecha de creación ascendente.
```

---

### **Etapa 3: Clarificación (`clarify.md`)**

#### **Propósito y Concepto**

Antes de pasar al diseño técnico, el equipo o el agente analiza la especificación en busca de ambigüedades, contradicciones, vacíos de lógica o conflictos con la constitución. Se formulan preguntas clave para cerrar todas las decisiones de negocio.

#### **Plantilla (`specs/NNN-slug/clarify.md`)**

```
# Registro de Clarificación: [Nombre de la Funcionalidad]

## Preguntas y Decisiones de Negocio
1. **Pregunta:** ¿Qué ocurre si dos tareas se crean con el mismo título?
   - **Decisión:** Se permiten títulos duplicados; la unicidad está dada por el UUID.
2. **Pregunta:** ¿Cómo debe responder el sistema si el archivo de datos está corrupto?
   - **Decisión:** Debe emitir una advertencia y crear una copia de respaldo antes de reiniciar.

## Requisitos Ajustados
- [Ajustes incorporados a la spec.md tras la clarificación]
```

---

### **Etapa 4: Planificación Técnica y Arquitectura (`plan.md`)**

#### **Propósito y Concepto**

Una vez cerrada la especificación funcional, esta fase traduce los requisitos en un diseño de ingeniería formal (el **CÓMO**). Define la arquitectura de módulos, los esquemas de datos (JSON Schema, esquemas SQL), contratos de integración y la estrategia de testing.

#### **Plantilla (`specs/NNN-slug/plan.md`)**

````
# Plan Técnico: [Nombre de la Funcionalidad]

## 1. Arquitectura de Módulos
- `src/core/domain.py`: Entidades puras y reglas de negocio.
- `src/storage/repository.py`: Adaptador de persistencia en disco.
- `src/cli/interface.py`: Analizador de comandos y formateador de consola.

## 2. Esquema de Datos (JSON Schema / DB)
```json
{
  "\$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "title": { "type": "string", "minLength": 1 },
    "status": { "enum": ["pending", "completed"] }
  },
  "required": ["id", "title", "status"]
}
```

## 3. Estrategia de Pruebas
- Pruebas unitarias para domain.py.
- Pruebas de integración con archivos temporales para repository.py.
````

---

### **Etapa 5: Descomposición en Tareas (`tasks.md`)**

#### **Propósito y Concepto**

El plan técnico se descompone en **unidades de trabajo atómicas**, independientes y ordenadas secuencialmente por dependencias. Cada tarea debe ser lo suficientemente pequeña como para ejecutarse dentro de un contexto limitado y asociarse directamente con los IDs de los requisitos de la especificación.

#### **Plantilla (`specs/NNN-slug/tasks.md`)**

```
# Plan de Ejecución de Tareas: [Nombre de la Funcionalidad]

- [ ] **Tarea 1: Estructura base y modelo de dominio**
  - **Depende de:** Ninguna
  - **Requisitos cubiertos:** RF-001
  - **Criterio de Aceptación:** Crear la clase `Task` con validación de título no vacío mediante pruebas unitarias.

- [ ] **Tarea 2: Capa de Persistencia JSON**
  - **Depende de:** Tarea 1
  - **Requisitos cubiertos:** RF-001, RF-003
  - **Criterio de Aceptación:** Implementar `TaskRepository.save()` y `TaskRepository.list_all()` pasando pruebas de integración en almacenamiento local.

- [ ] **Tarea 3: Interfaz CLI para adición de tareas**
  - **Depende de:** Tarea 2
  - **Requisitos cubiertos:** RF-002
  - **Criterio de Aceptación:** Manejar excepciones y mostrar mensaje de error en consola ante entradas inválidas.
```

---

### **Etapa 6: Implementación Guiada (`implement`)**

#### **Propósito y Concepto**

Se ejecuta el trabajo **tarea por tarea**. Si se utilizan agentes de IA o desarrolladores asistidos, cada sesión recibe únicamente la constitución, la especificación relevante, el plan técnico y la tarea específica en curso, asegurando que la generación de código permanezca estrictamente acotada.

#### **Flujo de Ejecución por Tarea (Bucle TDD)**

1. **Escribir prueba primero (Fase Roja):** Se redacta el test unitario basado en los criterios EARS de la tarea.
2. **Generar código mínimo (Fase Verde):** Se implementa el código fuente hasta que la prueba pase.
3. **Marcar casilla:** Se actualiza el estado de la tarea en `tasks.md` cambiando la casilla a `- [x]`.

---

### **Etapa 7: Validación de Contrato y Gobernanza Continua (`validate`)**

#### **Propósito y Concepto**

Verifica que el sistema construido cumpla al 100% con los criterios descritos en la especificación. Se ejecutan suites de prueba automatizadas, linters de contrato y validaciones de esquema.

Bajo el modelo **Spec-Anchored**, la especificación **no se desecha al entregar el código**; vive versionada en Git junto con la aplicación. Si en el futuro surge un cambio o error, **se actualiza primero la especificación** y luego se regenera o refactoriza el código, eliminando la deuda técnica y la divergencia de intención (_intent drift_).

#### **Plantilla (`specs/NNN-slug/validation_report.md`)**

```
# Reporte de Validación de Especificación

## Matriz de Trazabilidad
| ID Requisito | Criterio EARS | Prueba Asociada | Estado |
| :--- | :--- | :--- | :--- |
| **RF-001** | Creación con UUID | `tests/test_domain.py::test_create_task` | PASADO |
| **RF-002** | Manejo de título vacío | `tests/test_cli.py::test_empty_title_error` | PASADO |
| **RF-003** | Orden ascendente de lista | `tests/test_repo.py::test_list_ordering` | PASADO |

## Estado Final
- **Estatus:** ESPECIFICACIÓN CUMPLIDA AL 100%.
- **Acción:** Fusionar Pull Request e integrar spec viva en Git.
```

---
