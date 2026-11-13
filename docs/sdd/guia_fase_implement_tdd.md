# **Guía Integral: Ejecución, Protocolo TDD y Gobernanza de la Fase `Implement`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

La **fase de Implementación (`Implement`)** constituye la **Etapa 6** del ciclo de vida del **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**. Es el momento operativo en el que los requisitos funcionales (`spec.md`), la arquitectura técnica (`plan.md`) y el desglose de tareas (`tasks.md`) se transforman en **código fuente ejecutable y suites de prueba automatizadas**.

Frente a la programación imprecisa (_vibe coding_), en la que se pide a la Inteligencia Artificial generar bloques masivos de código a partir de instrucciones abiertas, la fase `Implement` opera bajo un **protocolo de ejecución acotado, determinista y gobernado por pruebas (TDD)**: ni el desarrollador ni el agente improvisan la arquitectura; ejecutan unidades discretas de trabajo tarea por tarea.

---

## **1\. Fundamentos y Propósito de la Fase `Implement`**

En los flujos de desarrollo asistidos por agentes de codificación, intentar programar una funcionalidad completa en una sola interacción provoca tres fallos sistemáticos: saturación de la ventana de contexto, alucinación de dependencias no autorizadas y divergencia de intención (_intent drift_).

La fase `Implement` resuelve estos problemas mediante cuatro pilares fundamentales:

1. **Aislamiento de Contexto por Tarea:** El modelo de IA o el programador concentra el 100% de su capacidad en resolver una única unidad de trabajo atómica (diseñada para completarse en 15 a 30 minutos), minimizando el consumo de tokens y evitando errores por dispersión.
2. **Desarrollo Guiado por Pruebas (TDD Estricto):** Ningún código de producción se genera sin una prueba automatizada previa que falle (fase Roja). Esto asegura que todo código resultante esté respaldado por criterios de aceptación ejecutables.
3. **Cumplimiento de Guardrails y Constitución:** La generación de código está estrictamente limitada a las dependencias, versiones y patrones arquitectónicos autorizados en `constitution.md` y `AGENTS.md`.
4. **Trazabilidad y Estado Transparente:** La finalización de cada tarea actualiza de inmediato el archivo `tasks.md` marcando la casilla de verificación (`- [x]`), permitiendo auditar el progreso en tiempo real.

---

## **2\. Rol en la Metodología de Desarrollo Basado en Especificaciones (SDD)**

Dentro del flujo de **7 etapas del SDD puro**, la implementación representa el puente ejecutor entre la descomposición de tareas y la validación final:

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
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │                    ETAPA 3: CLARIFICACIÓN (Clarify)                       │
 │  • specs/NNN-slug/clarify.md (Auditoría QA / Inspección de puntos ciegos)│
 └────────────────────────────────────┬──────────────────────────────────────┘
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
 │  • specs/NNN-slug/tasks.md (Desglose en unidades ejecutables acotadas) │
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
 └──────────────────────────────────────────────────────────────────────────┘
```

- **Insumo Obligatorio:** No se inicia la implementación sin contar con `tasks.md` aprobado y ordenado por dependencias.
- **Separación de Responsabilidades:** En `Implement` no se debate la arquitectura ni se modifican los requisitos de negocio; si durante la codificación se detecta un vacío técnico, el flujo se detiene y se retroalimenta la especificación o el plan antes de continuar.

---

## **3\. El Ciclo Operativo de Implementación (Bucle TDD Agéntico)**

La implementación se ejecuta como un protocolo iterativo tarea por tarea:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 1. Lectura y Selección de Tarea                                         │
 │    • Inspeccionar tasks.md y seleccionar la primera tarea libre (- [ ]).│
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 2. Fase Roja (Red): Escribir Prueba Automatizada                        │
 │    • Redactar el test unitario o de integración según el criterio EARS. │
 │    • Ejecutar la suite (pytest / vitest / etc) y confirmar que FAILS.   │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 3. Fase Verde (Green): Código Mínimo de Producción                      │
 │    • Escribir exclusivamente el código necesario para superar el test.  │
 │    • Ejecutar la suite y verificar que el test PASSES.                  │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 4. Fase Refactor & Lint: Limpieza y Tipado Estricto                     │
 │    • Aplicar linters y formateadores (ruff, mypy, eslint, etc).         │
 │    • Confirmar que todos los tests se mantengan en verde.               │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 5. Actualización de Artefacto y Detención                               │
 │    • Cambiar el estado de la tarea en tasks.md a (- [x]).               │
 │    • Pausar la ejecución antes de proceder con la siguiente tarea.      │
 └─────────────────────────────────────────────────────────────────────────┘
```

---

## **4\. Elementos Obligatorios de la Directiva de Implementación**

Para que un comando o prompt de implementación sea determinista, debe incluir los siguientes componentes en su contexto:

1. **Inyección de Contexto Estructurado:** Referencias directas a `@constitution.md`, `@spec.md`, `@plan.md` y `@tasks.md`.
2. **Identificador de Tarea Explícito:** Declaración de la tarea exacta a resolver (ej. `Tarea 2: Capa de persistencia JSON`).
3. **Mandato TDD Estricto:** Instrucción expresa de crear la prueba unitaria antes de tocar archivos de código de producción.
4. **Límites de Edición (_Scope Guardrails_):** Prohibición de modificar archivos ajenos a la tarea o añadir librerías no declaradas.
5. **Comando de Verificación de Entorno:** Comando exacto de terminal (`pytest tests/`, `npm test,` etc) para que el agente valide su propio trabajo.
6. **Regla de Marcado:** Obligación de actualizar la casilla a `- [x]` únicamente cuando los tests y linters pasen al 100%.

---

## **5\. Integración Operacional con OpenCode**

**OpenCode** optimiza la etapa de implementación a través de sus capacidades nativas:

- **Modo Construcción (`Build Mode`):** Mientras que la planificación se realiza en `Plan Mode` (`Shift + Tab`), la implementación requiere alternar a **`Build Mode`**, otorgando al agente permisos para crear archivos, refactorizar código y ejecutar comandos de terminal.
- **Comando Slash Personalizado (`/implement`):** Definido en `.opencode/commands/implement.md` para invocar el ciclo TDD automáticamente indicando la ruta del archivo de tareas.
- **Invocación por Referencia Directa (`@`):** Permite inyectar contexto quirúrgico en el chat:

```
/implement @specs/NNN-slug/tasks.md Tarea 1
```

- **Subagente Especializado (`@coder` / `@implementer`):** Se puede delegar la ejecución a un subagente con permisos de escritura y ejecución de comandos bash, mientras un subagente coordinador monitorea el progreso general definido en `.opencode/agents/`.

---

## **6\. Plantilla Optimizada y Estandarizada (`implement.md`)**

Esta plantilla se utiliza para estandarizar el comando agéntico en `.opencode/commands/implement.md` o como habilidad en `.opencode/skills/implement/SKILL.md`:

```
# implement.md (Ejemplo base)

# Directiva de Implementación Agéntica SDD

## Rol y Contexto Operativo
Eres el **Subagente Implementador (Implementer)**.
Tu función es transformar la tarea asignada en código probado y de alta calidad.
Antes de modificar archivos, consulta obligatoriamente:
- **Constitución:** `@docs/constitution.md`
- **Especificación Funcional:** `@specs/[id-feature]/spec.md`
- **Plan Técnico:** `@specs/[id-feature]/plan.md`
- **Plan de Tareas:** `@specs/[id-feature]/tasks.md`

## Objetivo
Implementar la **[ID_DE_TAREA]** indicada por el usuario siguiendo un flujo estricto de Desarrollo Guiado por Pruebas (TDD).

## Protocolo de Ejecución Paso a Paso

1. **Paso 1: Fase Roja (Test First)**
   - Crea o actualiza la suite de pruebas en `tests/` para cubrir los criterios de aceptación y requisitos `RF-xxx` de la tarea.
   - Ejecuta el comando de pruebas en la terminal y confirma que falle por la ausencia de la implementación.

2. **Paso 2: Fase Verde (Código Mínimo)**
   - Escribe el código de producción indispensable en `src/`.
   - Respeta estrictamente los esquemas, contratos de tipos y nombres de archivo definidos en `plan.md`.
   - No añadas funcionalidad extra no solicitada.

3. **Paso 3: Verificación y Calidad**
   - Ejecuta la suite de pruebas y confirma que el 100% pase.
   - Ejecuta los linters y chequeadores de tipo estático (`mypy`, `ruff`, `eslint`, `etc`).
   - Si se detecta algún error, corrige la implementación hasta resolverlo.

4. **Paso 4: Actualización de Estado**
   - Actualiza `@specs/[id-feature]/tasks.md` cambiando la casilla correspondiente de `- [ ]` a `- [x]`.
   - Reporta un resumen conciso con los archivos creados/modificados y los tests ejecutados.
   - **DETENTE**: No avances a la siguiente tarea sin confirmación explícita.
```

---

## **7\. Ejemplo Práctico: Ejecución de la Tarea 1 en OpenCode**

A continuación se muestra un ejemplo real de ejecución en la terminal de **OpenCode** implementando la **Tarea 1** del módulo "Exportación de Tareas a CSV":

### **Entrada del Usuario en la Terminal:**

```
/implement @specs/NNN-slug/tasks.md Tarea 1
```

### **Proceso Ejecutado por OpenCode (`Build Mode`):**

````
OpenCode (Build Mode) - Iniciando implementación...
✔ Contexto cargado: @docs/constitution.md
✔ Contexto cargado: @specs/NNN-slug/spec.md (Requisito RF-001, CB-001)
✔ Contexto cargado: @specs/NNN-slug/plan.md
✔ Tarea activa: Tarea 1 - Pruebas y Sanitización de Inyección CSV

[Paso 1/4] Creando prueba unitaria (Fase Roja)...
Creando archivo: tests/test_csv_exporter.py

```python
# tests/test_csv_exporter.py
from src.core.exporter import CSVTaskExporter

def test_sanitize_field_plain_text():
    assert CSVTaskExporter.sanitize_field("Tarea normal") == "Tarea normal"

def test_sanitize_field_formula_injection():
    assert CSVTaskExporter.sanitize_field("=SUM(A1:A10)") == "'=SUM(A1:A10)"
    assert CSVTaskExporter.sanitize_field("+12345") == "'+12345"
    assert CSVTaskExporter.sanitize_field("-descuento") == "'-descuento"
    assert CSVTaskExporter.sanitize_field("@admin") == "'@admin"
```

Ejecutando: pytest tests/test_csv_exporter.py
RESULTADO: FAILED (ModuleNotFoundError: No module named 'src.core.exporter')
✔ Fase Roja confirmada.

[Paso 2/4] Escribiendo código mínimo de producción (Fase Verde)...
Creando archivo: src/core/exporter.py

```python
# src/core/exporter.py

class CSVTaskExporter:
    @staticmethod
    def sanitize_field(value: str) -> str:
        """Sanitiza campos que inician con operadores de fórmula anteponiendo un apóstrofe."""
        if value and value in ('=', '+', '-', '@'):
            return f"'{value}"
        return value
```

[Paso 3/4] Verificando pruebas y tipos...
Ejecutando: pytest tests/test_csv_exporter.py
RESULTADO: 2 passed in 0.03s
Ejecutando: mypy src/core/exporter.py --strict
RESULTADO: Success: no issues found.

[Paso 4/4] Actualizando tareas...
Modificado: specs/NNN-slug/tasks.md
[x] Tarea 1: Pruebas y Sanitización de Inyección CSV (Core Exporter)

Resumen de Ejecución:
Creado src/core/exporter.py con método sanitize_field.
Pruebas unitarias en tests/test_csv_exporter.py aprobadas al 100%.
Requisito RF-001 y caso borde CB-001 cubiertos.

Tarea 1 completada. Ejecución pausada. ¿Proceder con la Tarea 2?
````

---
