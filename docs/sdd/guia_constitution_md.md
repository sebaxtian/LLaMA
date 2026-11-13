# **Guía Integral: Definición, Gobernanza e Integración de `constitution.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

En la metodología de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**, el archivo **`constitution.md`** constituye el documento supremo rector que establece los **principios innegociables**, las **restricciones de arquitectura**, los **estándares de calidad** y los **límites de seguridad (_guardrails_)** que rigen un proyecto.

A diferencia de las especificaciones funcionales que cambian con cada nueva funcionalidad (_feature_), la constitución actúa como la ley fundamental del repositorio, garantizando que tanto los desarrolladores humanos como los agentes de Inteligencia Artificial mantengan la coherencia técnica a lo largo del tiempo.

---

## **1\. Fundamentos y Propósito de `constitution.md`**

El archivo `constitution.md` resuelve el problema de la **divergencia de intención (_intent drift_)** y la degradación arquitectónica en entornos asistidos por IA. Cumple cuatro funciones críticas:

1. **Definir Límites Innegociables (_Guardrails_):** Declara con precisión qué librerías, dependencias, motores de persistencia o patrones arquitectónicos están autorizados o estrictamente prohibidos.
2. **Prevenir la Alucinación y la Deuda Técnica:** Evita que herramientas y agentes de codificación (como **OpenCode**, Claude Code o GitHub Copilot) introduzcan dependencias imprevistas, alteren esquemas de datos o rompan el aislamiento de capas (_vibe coding_).
3. **Establecer Criterios de Aceptación Universales:** Fija las normas de calidad obligatorias que todo código debe superar (por ejemplo, cobertura de pruebas unitarias o linters) antes de fusionarse.
4. **Alinear a Equipos y Agentes:** Sirve como la fuente única de verdad para la toma de decisiones técnicas de alto nivel, eliminando discusiones recurrentes sobre convenciones base.

---

## **2\. Rol en la Metodología de Desarrollo Basado en Especificaciones (SDD)**

En el ciclo de vida de **7 etapas del SDD puro**, `constitution.md` se ubica en el nivel más alto de la jerarquía normativa:

```
 ┌──────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                        │
 │  • docs/constitution.md ──► Principios innegociables y arquitectura      │
 │  • AGENTS.md            ──► System Prompt operativo y límites técnicos   │
 └────────────────────────────────────┬─────────────────────────────────────┘
                                      │
                                      ▼
                    [Etapas 2 a 7 del Flujo SDD]
        (spec.md ──► clarify.md ──► plan.md ──► tasks.md ──► ...)
```

- **Marco de Referencia para el Diseño:** Al redactar un plan técnico (`plan.md`) o descomponer tareas (`tasks.md`), el arquitecto o agente debe verificar que la propuesta no viole ningún principio constitucional.
- **Criterio de Validación Final:** Durante la **Etapa 7 (Validación)**, el subagente de auditoría revisa el código generado contrastándolo directamente con los mandatos de `constitution.md`.
- **Momento de Creación:** Se redacta de forma obligatoria en la **Etapa 1 (Setup del Proyecto)**. Aunque es un documento vivo versionado en Git, sus modificaciones requieren consenso formal del equipo.

---

## **3\. Principios de Redacción y Estructura Técnica**

Para asegurar que sea procesable sin ambigüedades por humanos y modelos de lenguaje, `constitution.md` debe construirse bajo tres pautas de diseño determinista:

- **Ubicación en el Repositorio:** Se almacena convencionalmente en `docs/constitution.md` (o en la raíz `/constitution.md`).
- **Estilo Imperativo y Verificable:** Utiliza oraciones directas, afirmativas y con identificadores claros (ej. `PRINCIPIO-01`), evitando términos vagos como _"intentar"_ o _"en lo posible"_.
- **Jerarquía Superior:** En caso de contradicción entre una especificación funcional (`spec.md`) y la Constitución, **la Constitución siempre prevalece** hasta que se apruebe una enmienda formal.

### **Elementos Obligatorios que debe Contener:**

1. **Principios Innegociables:** Mandatos de máxima prioridad (ej. _"La especificación manda sobre el código"_, _"Aislamiento total del dominio"_).
2. **Stack Tecnológico y Restricciones:** Versión exacta del lenguaje/runtime, base de datos y lista blanca de frameworks permitidos.
3. **Límites Arquitectónicos:** Reglas de separación de capas (dominio puro sin dependencias de I/O, adaptadores desacoplados).
4. **Normas de Calidad y Testing:** Políticas de TDD, tipos de prueba exigidos y notación formal para requisitos (como EARS).
5. **Convenciones de Idioma:** Definición explícita de idiomas para código, comentarios, mensajes de error e interfaces.
6. **Protocolo de Enmiendas:** Procedimiento formal para actualizar la constitución cuando el proyecto evolucione.

---

## **4\. Integración Operacional con OpenCode**

**OpenCode** interactúa de forma nativa con `constitution.md` mediante el siguiente flujo de trabajo:

- **Punto de Enlace vía `AGENTS.md`:** Al iniciar sesión con **OpenCode**, el agente lee `AGENTS.md`, el cual contiene una directiva imperativa: _"Leer y cumplir estrictamente `docs/constitution.md` antes de proponer planes o modificar código"_.
- **Restricción en Modo Planificación (`Plan Mode`):** Al ejecutar el comando `/plan` o diseñar un incremento técnico, **OpenCode** consulta la constitución para descartar arquitecturas o librerías no autorizadas.
- **Auditoría con Subagentes (`@reviewer`):** Permite configurar subagentes de solo lectura en `.opencode/agents/reviewer.md` cuya misión exclusiva sea auditar que el código generado no vulnere ninguno de los principios constitucionales antes del merge.

---

## **5\. Plantilla Optimizada y Estandarizada (`docs/constitution.md`)**

```
# constitution.md (Ejemplo base)

# Constitución del Proyecto: [Nombre del Proyecto]

## 1. Principios Innegociables
- **PRINCIPIO-1 (La Spec Manda):** Ninguna línea de código de producción se escribe sin una especificación formal previa aprobada. Si el código diverge de la spec, el código es incorrecto.
- **PRINCIPIO-2 (Aislamiento de Dominio):** La lógica de negocio principal (núcleo) debe ser pura y desacoplada. Queda prohibida la importación de librerías de I/O, frameworks web o bases de datos dentro de los modelos de dominio.
- **PRINCIPIO-3 (Verificabilidad Automatizada):** Todo requisito funcional o caso de borde debe contar con una prueba automatizada asociada que garantice su cumplimiento.

## 2. Stack Tecnológico y Restricciones
- **Lenguaje y Runtime:** [ej. Python 3.12 con tipado estricto (`mypy --strict`) / TypeScript 5.x]
- **Persistencia de Datos:** [ej. PostgreSQL 16 con migraciones en código / Archivo JSON local aislado]
- **Librerías Autorizadas:** Uso exclusivo de las dependencias declaradas en el gestor de paquetes oficial (`pyproject.toml` / `package.json`). Queda prohibida la instalación imprevista de librerías de terceros.

## 3. Normas de Calidad y Sintaxis de Requisitos
- Todos los requisitos funcionales de las especificaciones deben redactarse utilizando la sintaxis **EARS** (*Easy Approach to Requirements Syntax*).
- Formateo de código y linters automatizados obligatorios antes de cada commit.
- Cobertura de pruebas exigida sobre la lógica central antes de dar por completada una tarea.

## 4. Convenciones de Idioma
- **Código y Comentarios:** Inglés técnico obligatorio para nombres de variables, funciones, clases, commits y documentación técnica interna.
- **Interfaz y Mensajes de Usuario:** [Español / Idioma del producto] para mensajes de consola, logs de usuario final e interfaces visuales.

## 5. Gobernanza y Protocolo de Enmiendas
- Cualquier cambio estructural o modificación del stack tecnológico requiere una enmienda explícita en este documento antes de proceder a la actualización de especificaciones o código fuente.
```

---

## **6\. Ejemplo Práctico: Proyecto CLI `StudyTracker` en Python con OpenCode**

A continuación se presenta un ejemplo real del archivo `docs/constitution.md` para un gestor de hábitos y sesiones de estudio desarrollado con **OpenCode**:

```
# constitution.md (Ejemplo base)

# Constitución del Proyecto: StudyTracker CLI

## 1. Principios Innegociables
- **P-01 (Simplicidad y Robustez):** El sistema es una herramienta CLI educativa que debe mantenerse ligera, determinista y comprensible sin dependencias innecesarias.
- **P-02 (La Spec Manda):** Toda nueva funcionalidad debe iniciar en `specs/` con sus correspondientes `spec.md` y `plan.md` antes de generar código fuente.
- **P-03 (Separación Estricta de Capas):** El módulo de cálculo de racha, tiempos y estadísticas debe ser completamente independiente de la interfaz de consola (`argparse`) y del mecanismo de almacenamiento.
- **P-04 (Disciplina de Pruebas):** Toda regla de cálculo temporal o manipulación de fechas debe probarse al 100% mediante suites de `pytest`.
- **P-05 (Flujo de Trabajo Git):** Fuerte en determinismo Git (docs/Flujo_de_Trabajo_Git.md)

## 2. Stack Tecnológico y Restricciones
- **Lenguaje:** Python 3.12 con verificación de tipos estáticos (`mypy --strict`).
- **Persistencia:** Archivo local JSON aislado en el directorio del usuario (`~/.study_tracker.json`).
- **Dependencias Prohibidas:** No se autoriza el uso de frameworks CLI pesados (como Click o Typer) ni de ORMs externos; se debe emplear exclusivamente la biblioteca estándar de Python, reservando dependencias externas solo para herramientas de desarrollo (`pytest`, `ruff`, `mypy`).

## 3. Idioma y Formato
- **Código Fuente:** Nombres de módulos, clases, variables y tests redactados estrictamente en inglés (`study_session.py`, `test_streak_calculator.py`).
- **Interacción de Usuario:** Mensajes de consola, menú de ayuda y textos de error redactados en español.

## 4. Reglas de Ejecución Agéntica para OpenCode
- OpenCode debe ejecutar la suite de `pytest` y confirmar que el 100% de las pruebas pasen antes de marcar cualquier tarea como completada en `tasks.md`.
- Queda prohibido modificar la estructura del archivo JSON de almacenamiento sin haber actualizado previamente el esquema de datos en el plan técnico correspondiente.
```

---
