# **Guía Integral: Definición, Control de Calidad e Integración de `clarify.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El archivo **`clarify.md`** (o proceso de **Clarificación**) representa la **fase de inspección, control de calidad y resolución de ambigüedades** siendo determinista dentro de la metodología de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**.

Actúa como una barrera de control que audita la especificación funcional (`spec.md`) antes de autorizar el diseño técnico (`plan.md`). Su propósito es detectar vacíos de lógica, requisitos imprecisos, situaciones límite (_edge cases_) no contempladas, contradicciones internas o conflictos con la constitución del repositorio (`constitution.md`), sustituyendo las suposiciones por decisiones de negocio documentadas deterministas.

---

## **1\. Fundamentos y Propósito de `clarify.md`**

En los flujos de desarrollo asistidos por Inteligencia Artificial, el mayor riesgo no reside en la velocidad de escritura de código, sino en la **divergencia de intención (_intent drift_)** originada por requisitos ambiguos y no deterministas. Si un modelo de lenguaje o un desarrollador recibe una especificación con vacíos lógicos, tenderá a improvisar o asumir comportamientos (_vibe coding_).

`clarify.md` resuelve este problema cumpliendo cuatro objetivos esenciales:

1. **Eliminación Total de Suposiciones (_Zero-Assumption Policy_):** Fuerza al equipo o a la IA a identificar dudas funcionales y formular preguntas explícitas antes de escribir una sola línea de código o diseñar tablas de base de datos.
2. **Detección Temprana de Casos Límite (_Edge Cases_):** Descubre escenarios de excepción, límites numéricos, fallos de conectividad o combinaciones de datos no contempladas en la redacción inicial del producto.
3. **Optimización de Costos de Corrección:** Resolver una ambigüedad durante la fase de clarificación toma minutos de conversación; corregir una asunción errónea cuando ya se crearon migraciones de base de datos y lógica de negocio cuesta días.
4. **Registro Histórico de Decisiones de Producto (ADR Funcional):** Documenta formalmente por qué se adoptó determinada regla de negocio ante una disyuntiva, evitando debates recurrentes en el futuro.

---

## **2\. Rol en la Metodología de Desarrollo Basado en Especificaciones (SDD)**

En el ciclo de vida de **7 etapas del SDD puro**, la clarificación se ubica estratégicamente en la **Etapa 3**, sirviendo como puente de validación entre el **QUÉ** funcional y el **CÓMO** técnico:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • docs/constitution.md (Principios innegociables y arquitectura)       │
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
 └─────────────────────────────────────────────────────────────────────────┘
```

- **Criterio de Paso (_Quality Gate_):** No se autoriza la redacción del plan técnico (`plan.md`) ni la creación de esquemas de datos hasta que el reporte de clarificación se marque como cerrado y sus decisiones hayan sido retroalimentadas en `spec.md`.
- **Aislamiento de Responsabilidades:** `clarify.md` audita exclusivamente el comportamiento funcional y de negocio. No debe discutir nombres de clases, librerías externas o detalles de implementación; eso corresponde a la etapa de planificación técnica.

---

## **3\. Principios de Diseño y Estructura Técnica**

Para mantener la claridad del proceso, `clarify.md` se gestiona siguiendo estas pautas:

- **Ubicación en el Repositorio:** Se almacena dentro de la carpeta asignada a la funcionalidad en `specs/` (por ejemplo, `specs/NNN-slug/clarify.md` o `specs/002-user-auth/clarify.md`).
- **Naturaleza Bidireccional:** El archivo es a la vez un registro interactivo de preguntas y respuestas (durante la sesión con la IA o Product Owner) y un documento de auditoría permanente tras la aprobación.
- **Ciclo de Parches:** Toda decisión tomada en `clarify.md` debe derivar en una actualización directa sobre los requisitos funcionales de `spec.md` (ajustando o agregando cláusulas EARS).

### **Elementos Obligatorios que debe Contener:**

1. **Información General y Referencias:** ID de la característica, ruta de la especificación auditada y estado de la inspección.
2. **Hallazgos y Ambigüedades Detectadas:** Lista numerada de inconsistencias, vacíos de especificación o contradicciones encontradas.
3. **Registro de Preguntas y Decisiones (Q\&A de Negocio):** Transcripción estructurada de las preguntas formuladas y las decisiones tomadas por el responsable del producto o desarrollador.
4. **Nuevos Casos Borde Identificados:** Escenarios de excepción formalizados con su correspondiente impacto funcional.
5. **Matriz de Parches Requeridos:** Lista de verificación (_checklist_) que certifica qué secciones o requisitos de `spec.md` fueron modificados para reflejar las decisiones.

---

## **4\. Integración Operacional con OpenCode**

**OpenCode** optimiza el flujo de clarificación mediante sus modos y extensiones modulares:

- **Comando Slash Dedicado (`/clarify` o `/sdd-clarify`):** Se define un comando en `.opencode/commands/clarify.md` que instruye al modelo a leer `@docs/constitution.md` y `@specs/NNN-slug/spec.md`, adoptar el rol de un auditor QA senior y formular preguntas estructuradas al desarrollador en la terminal (TUI).
- **Subagente de Inspección (_Reviewer / Clarifier_):** Puede ejecutarse mediante un subagente de solo lectura (`read-only`), garantizando que la IA razone sobre los vacíos del negocio sin generar código prematuro.
- **Sincronización Automatizada:** Una vez respondidas las preguntas en la sesión interactiva, **OpenCode** genera el archivo `clarify.md` y actualiza automáticamente los requisitos funcionales y casos límite dentro de `spec.md`.

---

## **5\. Plantilla Optimizada y Estandarizada (`clarify.md`)**

```
# clarify.md (Ejemplo base)

# Registro de Clarificación: [Nombre de la Funcionalidad]

## 1. Información General
- **Especificación Evaluada:** `specs/[id-feature]/spec.md`
- **Constitución de Referencia:** `docs/constitution.md`
- **Fecha de Inspección:** [AAAA-MM-DD]
- **Estatus:** [En Progreso / Completado - Decisiones Aprobadas]

---

## 2. Hallazgos y Ambigüedades Detectadas
- **AMB-001:** [Descripción concisa del vacío de lógica o ambigüedad detectada].
- **AMB-002:** [Descripción de la contradicción o caso límite no contemplado].

---

## 3. Preguntas y Decisiones de Negocio (Q&A)

### Pregunta 1: [Tema o Componente Evaluado]
- **Pregunta formulada por la IA/QA:** ¿[Pregunta concreta sobre el comportamiento del sistema ante un escenario específico]?
- **Opciones consideradas:**
  - Opción A: [Descripción breve].
  - Opción B: [Descripción breve].
- **Decisión del Negocio:** [Opción seleccionada y justificación de la regla].

### Pregunta 2: [Tema o Componente Evaluado]
- **Pregunta formulada por la IA/QA:** ¿[Pregunta concreta sobre manejo de errores o excepciones]?
- **Decisión del Negocio:** [Respuesta explícita y regla operativa adoptada].

---

## 4. Nuevos Casos Borde Identificados
- **CB-NUEVO-01:** Si [condición límite o fallo imprevisto], entonces el [sistema] debe [respuesta del sistema].

---

## 5. Lista de Parches Aplicados a `spec.md`
- [ ] Actualizar **RF-00X** en `spec.md` incorporando la decisión tomada en la Pregunta 1.
- [ ] Agregar **CB-NUEVO-01** a la sección de Casos Borde de `spec.md`.
- [ ] Confirmar que no existen contradicciones con `docs/constitution.md`.
```

---

## **6\. Ejemplo Práctico: Clarificación para "Exportación de Tareas a CSV"**

A continuación se muestra un ejemplo real del archivo `specs/NNN-slug/clarify.md` procesado dentro de OpenCode para el módulo de exportación CSV:

```
# clarify.md (Ejemplo base)

# Registro de Clarificación: Exportación de Tareas a CSV

## 1. Información General
- **Especificación Evaluada:** `specs/NNN-slug/spec.md`
- **Constitución de Referencia:** `docs/constitution.md`
- **Fecha de Inspección:** 2026-10-29
- **Estatus:** Completado - Decisiones Aprobadas

---

## 2. Hallazgos y Ambigüedades Detectadas
- **AMB-001:** La `spec.md` indicaba que se debían exportar "las tareas filtradas", pero no definía si la exportación respetaba la paginación visible en pantalla (ej. 10 registros) o la totalidad de los datos que cumplen el criterio en la base de datos.
- **AMB-002:** No se especificaba el tratamiento de caracteres conflictivos en el formato CSV (como comas internas, saltos de línea o comillas) dentro del título de la tarea.
- **AMB-003:** No se contemplaba la vulnerabilidad de inyección CSV en aplicaciones de hojas de cálculo (Excel/Google Sheets) si un título inicia con operadores de fórmula.

---

## 3. Preguntas y Decisiones de Negocio (Q&A)

### Pregunta 1: Alcance del Conjunto de Datos a Exportar
- **Pregunta formulada por OpenCode:** Cuando el usuario tiene aplicada una vista paginada (ej. viendo 10 de 100 tareas filtradas), ¿el archivo CSV debe contener únicamente las 10 tareas de la página actual o el universo completo de las 100 tareas coincidentes?
- **Decisión del Negocio:** El archivo CSV debe exportar el **universo completo de registros filtrados (las 100 tareas)**, ignorando la paginación de la interfaz de usuario.

### Pregunta 2: Estandarización de Formato y Delimitadores
- **Pregunta formulada por OpenCode:** ¿Cómo deben estructurarse los campos que contengan comas o comillas dobles?
- **Decisión del Negocio:** Se debe cumplir estrictamente con el estándar **RFC 4180**: cualquier campo que contenga comas o saltos de línea debe envolverse entre comillas dobles, y las comillas dobles internas deben escaparse duplicándolas (`""`).

### Pregunta 3: Seguridad ante Inyección CSV (*Formula Injection*)
- **Pregunta formulada por OpenCode:** ¿Cómo debe reaccionar el sistema si el título de una tarea comienza con caracteres de fórmula como `=`, `+`, `-` o `@`?
- **Decisión del Negocio:** El sistema debe sanitizar el campo anteponiendo un apóstrofe inicial (`'`) para forzar a las hojas de cálculo a interpretar el valor como texto plano.

---

## 4. Nuevos Casos Borde Identificados
- **CB-001 (Inyección CSV):** Si el título de una tarea comienza con los caracteres `=`, `+`, `-` o `@`, el sistema debe anteponer un apóstrofe (`'`) antes de generar la fila del CSV.
- **CB-002 (Concurrencia durante la Exportación):** Si se crean o eliminan tareas mientras el proceso de exportación está en ejecución, el archivo debe reflejar el estado consistente al momento exacto en que se inició la solicitud.

---

## 5. Lista de Parches Aplicados a `spec.md`
- [x] Ajustado **RF-001** en `spec.md` para especificar que la exportación aplica sobre el universo completo de registros filtrados y no sobre la página activa.
- [x] Agregada la referencia de cumplimiento al estándar **RFC 4180** en **RF-002**.
- [x] Incorporado **CB-001** en la sección de Casos Borde de `spec.md`.
```

---
