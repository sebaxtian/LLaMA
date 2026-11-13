# **Guía Integral: Definición, Arquitectura y Gobernanza Técnica de `plan.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El archivo **`plan.md`** (o `TECHNICAL-SPEC.md` / `architecture.md`) representa el **diseño técnico y plan de arquitectura** de un incremento o funcionalidad dentro de la metodología de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**.

Mientras que el archivo `spec.md` define el **QUÉ** necesita el negocio, `plan.md` establece el **CÓMO** técnico para construirlo.

---

## **1\. ¿Qué es `plan.md`?**

**`plan.md`** es el documento que traduce los requisitos funcionales de negocio (validados en `spec.md` y clarificados en `clarify.md`) en un **diseño de ingeniería de software formal, concreto y estructurado**.

En el SDD puro, `plan.md` actúa como la **fuente de verdad técnica**. Describe la arquitectura de módulos, la estructura de directorios, los esquemas de datos (JSON Schema, tablas SQL, DTOs), las firmas de interfaz/API, los algoritmos internos, las decisiones tecnológicas (ADRs) y la estrategia de pruebas automatizadas.

---

## **2\. Casos de Uso Principales**

- **Traducción de intención a arquitectura:** Actúa como puente obligatorio entre la visión de producto y la generación de código fuente.
- **Definición de contratos y esquemas de datos:** Establece tipos de datos explícitos, modelos de base de datos y contratos de entrada/salida para que los componentes puedan ser probados o emulados (_mocks_) en paralelo.
- **Aislamiento de contexto y límites para la IA (_Guardrails_):** Evita que agentes de IA (como **OpenCode**, Claude Code o GitHub Copilot) adivinen la estructura de carpetas, introduzcan librerías no autorizadas o utilicen patrones de diseño incompatibles con la base de código existente.
- **Trazabilidad de decisiones técnicas (ADRs):** Justifica por qué se eligieron ciertas bibliotecas, algoritmos o estructuras de persistencia, dejando un registro histórico técnico en Git.

---

## **3\. Principios de Definición de `plan.md`**

- **Ubicación en el repositorio:** Se almacena junto con los demás artefactos de la característica en `specs/` (por ejemplo, `specs/NNN-slug/plan.md` o `specs/002-auth-login/plan.md`).
- **Enfoque puramente técnico:** A diferencia de `spec.md` (que utiliza lenguaje funcional de negocio), `plan.md` emplea terminología técnica de ingeniería: nombres de archivos, módulos, clases, interfaces, tipos, comandos de consola y esquemas formales.
- **Sujeto a la Constitución:** Debe cumplir estrictamente con los principios innegociables y el _stack_ tecnológico autorizado definidos previamente en `docs/constitution.md`.

---

## **4\. Elementos e Información Obligatoria que debe Contener**

1. **Contexto Técnico y Referencias:** Enlaces directos a `constitution.md`, `spec.md` y al registro `clarify.md` de la característica.
2. **Estructura de Módulos y Archivos:** Mapa explícito de carpetas y archivos que se crearán o modificarán en la base de código (`src/core/`, `src/storage/`, `tests/`, etc.).
3. **Esquema de Datos y Modelos:** Definición formal de estructuras de datos mediante JSON Schema, esquemas SQL, DTOs o interfaces del lenguaje elegido.
4. **Contratos de Interfaces y API:** Firmas de funciones principales, endpoints de API (OpenAPI/TypeSpec), parámetros de entrada, valores de retorno y excepciones técnicas.
5. **Decisiones Técnicas y Algoritmos (ADRs locales):** Explicación de la lógica de procesamiento (ej. algoritmo de cálculo, estrategias de ordenamiento o escaping de seguridad).
6. **Estrategia de Testing y Verificación:** Plan de pruebas unitarias, de integración y de contrato bajo enfoque TDD/BDD.

---

## **5\. Función en la Metodología SDD y Ubicación en el Flujo**

Dentro del flujo de **7 etapas del SDD puro**, la planificación técnica corresponde a la **Etapa 4: Planificación (_Plan_)**:

```
[Etapa 1: Constitution (constitution.md) & AGENTS.md]  ──► Reglas generales y límites del repo
              │
              ▼
[Etapa 2: Specify (spec.md)]         ──► Requisitos de negocio (QUÉ y POR QUÉ)
              │
              ▼
[Etapa 3: Clarify (clarify.md)]      ──► Inspección QA, vacíos y ambigüedades
              │
              ▼
[Etapa 4: Plan (plan.md)]            ──► Arquitectura técnica y esquemas (CÓMO)
              │
              ▼
[Etapa 5: Tasks (tasks.md)]           ──► Desglose en tareas atómicas e independientes
              │
              ▼
[Etapa 6: Implement]                  ──► Ejecución TDD + Código fuente
              │
              ▼
[Etapa 7: Validate]                   ──► Verificación de contrato contra la spec
```

**Función Clave**: Convertir la intención de negocio validada en la arquitectura de código necesaria para descomponer el trabajo en tareas atómicas (tasks.md) en la siguiente etapa.

---

## **6\. Integración de `plan.md` con OpenCode**

**OpenCode** ofrece soporte agéntico directo para la creación y consumo de `plan.md`:

- **Modo Plan Nativo (_Plan Mode_ / `Shift + Tab`):** OpenCode cuenta con un agente primario `plan` diseñado específicamente para explorar la base de código, razonar sobre la arquitectura y formular el plan técnico **sin modificar código fuente de forma intempestiva**.
- **Generación mediante Comandos Slash (`/plan` o `/sdd-plan`):** Se pueden definir comandos personalizados en `.opencode/commands/` o usar configuraciones de Spec Kit / OpenSpec para que OpenCode lea `@docs/constitution.md`, `@spec.md` y `@clarify.md` y redacte automáticamente `plan.md`.
- **Referencia con `@` en Terminal:** Durante la fase de desarrollo, el desarrollador o agente puede inyectar el plan como contexto activo invocando `@specs/NNN-slug/plan.md` en la terminal (TUI) de OpenCode.
- **Subagente Arquitecto (_AllePlanner_ / `planner`):** Permite ejecutar un subagente de solo lectura en **OpenCode** cuya única función es auditar el diseño técnico antes de autorizar el desglose de tareas.

---

## **7\. Plantilla Optimizada y Estandarizada (`plan.md`)**

````
# plan.md (Ejemplo base)

# Plan Técnico: [Nombre de la Funcionalidad]

## 1. Referencias y Contexto
- **Constitución:** `docs/constitution.md`
- **Especificación Funcional:** `specs/[id-feature]/spec.md`
- **Registro de Clarificación:** `specs/[id-feature]/clarify.md`

## 2. Arquitectura de Módulos y Estructura de Directorios
- `src/core/[modulo].py`: Lógica de dominio pura y reglas de cálculo.
- `src/storage/[repositorio].py`: Adaptador de persistencia o lectura/escritura.
- `src/cli/[interfaz].py`: Parsing de argumentos y formateo de salida.
- `tests/test_[modulo].py`: Pruebas unitarias de dominio e integración.

## 3. Esquemas de Datos y Tipos (JSON Schema / Type Definitions)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EstructuraDeDatos",
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "campo_clave": { "type": "string", "minLength": 1 }
  },
  "required": ["id", "campo_clave"]
}
```

## 4. Interfaces y Contrato de Componentes
- ClasePrincipal.metodo_clave(param: Tipo) -> Resultado: Descripción del comportamiento técnico.
- Manejo de Excepciones: Lanzar ExcepcionDominio ante fallos de validación interna.

## 5. Algoritmos y Decisiones Técnicas (ADR Local)
- Decisión 1: Usar biblioteca estándar csv y la norma RFC 4180 para empaquetado de campos.
- Decisión 2: Aplicar filtro directo sobre la persistencia para evitar cargar datasets grandes en memoria.

## 6. Estrategia de Testing (TDD)
- Pruebas Unitarias: Cubrir el 100% de los casos borde identificados en spec.md y clarify.md.
- Pruebas de Integración: Verificar la creación física de archivos o registros temporales mediante accesorios de prueba (fixtures).
````

---

## **8\. Ejemplo Práctico: Plan Técnico para "Exportación de Tareas a CSV"**

A continuación se presenta un ejemplo real del archivo \`specs/NNN-slug/plan.md\` generado para un sistema CLI en Python con OpenCode:

````
# plan.md (Ejemplo base)

# Plan Técnico: Exportación de Tareas a CSV

## 1. Referencias y Contexto
- **Constitución:** `docs/constitution.md` (Aislamiento de dominio, Python 3.12 strict typing)
- **Especificación Funcional:** `specs/NNN-slug/spec.md` (Requisitos RF-001 a RF-004)
- **Registro de Clarificación:** `specs/NNN-slug/clarify.md` (Decisión de exportar dataset completo no paginado y sanitizar inyecciones)

## 2. Arquitectura de Módulos y Estructura de Directorios
- `src/core/exporter.py`: Módulo con la clase `CSVTaskExporter` encargada del formateo y escape RFC 4180.
- `src/storage/task_repository.py`: Extensión del método `get_all_filtered(status: str) -> list[Task]`.
- `src/cli/commands.py`: Comando `export-csv` en la CLI que verifica permisos del usuario activo.
- `tests/test_csv_exporter.py`: Suite de pruebas unitarias para formateo, headers e inyección CSV.

## 3. Esquema de Datos del CSV
Los archivos generados deben cumplir con la siguiente estructura de columnas:

| Posición | Nombre Columna | Tipo de Dato | Formato / Regla de Formateo |
| :--- | :--- | :--- | :--- |
| 1 | `id` | UUID String | Identificador único estándar |
| 2 | `titulo` | String | Sanitizado ante caracteres `=`, `+`, `-`, `@` |
| 3 | `estado` | Enum String | `pending` \| `completed` |
| 4 | `fecha_creacion` | ISO 8601 String | `YYYY-MM-DDTHH:MM:SSZ` |

## 4. Interfaces y Contratos de Código

```python
# src/core/exporter.py
from typing import List
from src.core.models import Task

class CSVTaskExporter:
    @staticmethod
    def sanitize_field(value: str) -> str:
        """Si el valor inicia con =, +, -, @, antepone un apóstrofe ' para prevenir inyección CSV."""
        if value and value in ('=', '+', '-', '@'):
            return f"'{value}"
        return value

    def generate_csv_content(self, tasks: List[Task]) -> str:
        """Genera la cadena de texto CSV codificada en UTF-8 con la fila de encabezado."""
        pass
```

## 5. Decisiones Técnicas y Algoritmos (ADR)
- Sanitización de Inyección CSV: Para cumplir con el caso borde CB-001 de clarify.md, sanitize_field() evalúa el primer carácter del título. Si es un operador de fórmula, antepone un apóstrofe ' asegurando que Excel o Google Sheets lo interpreten como texto plano.
- Uso de io.StringIO: El contenido CSV se compilará primero en memoria usando io.StringIO y el módulo nativo csv.writer(quoting=csv.QUOTE_MINIMAL) antes de escribirse en disco o enviarse a la salida estándar.

## 6. Estrategia de Testing (TDD)
- tests/test_csv_exporter.py::test_header_generation: Verifica la presencia de los 4 encabezados exactos aun con lista vacía (RF-003).
- tests/test_csv_exporter.py::test_csv_injection_prevention: Prueba la sanitización para títulos como =SUM(A1:A10) -> '=SUM(A1:A10).
- tests/test_cli_export.py::test_unauthorized_user_blocked: Verifica el rechazo de permiso para usuarios con rol estándar (RF-004).
````

---
