# **Guía Integral: Definición, Gobernanza e Integración de Skills en Entornos Agénticos y SDD**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

Las **Skills** (Habilidades de Agente) representan un estándar abierto e interoperable de la industria adoptado por plataformas agénticas de vanguardia (tales como **OpenCode**, Claude Code, Cursor, GitHub Copilot y OpenAI Codex) para dotar a los modelos de lenguaje de **capacidades procedimentales, flujos de trabajo repetibles y conocimientos técnicos especializados bajo demanda**.

A diferencia del archivo `AGENTS.md` —que actúa como un _System Prompt_ persistente y global cargado obligatoriamente en cada inicio de sesión—, las Skills se rigen bajo el principio arquitectónico de **divulgación progresiva (_Progressive Disclosure_)**, garantizando que el agente solo consuma contexto y tokens cuando la tarea en curso lo requiera estrictamente.

---

## **1\. Fundamentos y Principio de Divulgación Progresiva (_Progressive Disclosure_)**

Uno de los principales cuellos de botella en el desarrollo de software asistido por Inteligencia Artificial es la **saturación y degradación de la ventana de contexto**. Cargar en cada interacción manuales exhaustivos sobre cada librería, framework o proceso del proyecto eleva drásticamente los costos operativos, ralentiza la inferencia y aumenta la probabilidad de alucinaciones.

Las **Skills** resuelven este problema mediante un mecanismo de activación en dos fases:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ FASE 1: ARRANQUE E INDEXACIÓN LIVIANA (~50 tokens por Skill)            │
 │ • El agente lee únicamente el Frontmatter YAML (name y description).    │
 │ • Registra en su catálogo interno qué habilidades tiene disponibles.    │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                         ¿La tarea actual coincide
                         con la descripción de la Skill?
                                      │
                       SÍ ────────────┴──────────── NO
                       │                            │
                       ▼                            ▼
 ┌──────────────────────────────────────────┐  ┌─────────────────────────┐
 │ FASE 2: CARGA EN CALIENTE                │  │ REPOSO                  │
 │ (500 a 5,000 tokens bajo demanda)        │  │ La Skill permanece      │
 │ • Inyecta el cuerpo completo (SKILL.md). │  │ descargada de memoria.  │
 │ • Aplica los patrones y restricciones.   │  └─────────────────────────┘
 └──────────────────────────────────────────┘
```

Indexación Liviana (Fase de Reposo): En el arranque del espacio de trabajo, el agente analiza únicamente los metadatos de cabecera (name y description) de cada habilidad encontrada en el árbol de directorios, consumiendo apenas \~50 tokens por archivo.

1. **Carga en Caliente (Fase Activa):** Cuando el usuario o el flujo de trabajo introduce un objetivo que coincide semánticamente con la descripción de la habilidad, el agente carga el contenido completo de `SKILL.md` (de 500 a más de 5,000 tokens), aplica sus directrices operativas y ejecuta la tarea con precisión quirúrgica.

---

## **2\. Casos de Uso Principales**

- **Estandarización de Guías de Diseño y Frontend:** Inyectar convenciones visuales avanzadas (ej. `frontend-design`), reglas de Tailwind CSS v4, directrices de accesibilidad (WCAG) o diseño de microinteracciones sin sobrecargar las consultas generales del backend.
- **Encapsulación de Procedimientos Repetitivos:** Automatizar flujos de trabajo complejos como el ciclo de Desarrollo Guiado por Pruebas (TDD), refactorizaciones seguras de base de datos o migraciones de contratos API.
- **Manejo Especializado de Dominio Técnico:** Enseñar a la IA a interactuar con precisión con herramientas complejas (como TypeSpec, Schemathesis, Prisma o Supabase) aplicando patrones idiomáticos aprobados por el equipo.
- **Gobernanza de Fechas, Tiempos y Zonas Horarias:** Establecer reglas estrictas para el formateo temporal, cálculos de rachas y almacenamiento determinista en UTC (ej. habilidad `local-dates`).

---

## **3\. Rol de las Skills en la Metodología SDD (_Spec-Driven Development_)**

Dentro del marco del **Desarrollo Basado en Especificaciones (SDD)** puro, existe una clara división de responsabilidades entre los distintos artefactos del proyecto:

- **`constitution.md` y `AGENTS.md`:** Establecen los límites innegociables, las prohibiciones y las directrices globales del repositorio.
- **`spec.md`:** Especifica el **QUÉ** funcional de negocio mediante requisitos en notación **EARS**.
- **`plan.md`:** Diseña el **CÓMO** técnico estructural (esquemas de datos, contratos y arquitectura de módulos).
- **Skills (`SKILL.md`):** Estandarizan el **CÓMO PROCEDIMENTAL**. Definen las mejores prácticas de codificación, los comandos de terminal autorizados y el protocolo que la IA debe respetar al transformar una especificación en software funcional.

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • docs/constitution.md (Leyes fundamentales)                           │
 │  • AGENTS.md (Punto de entrada general)                                 │
 │  • .agents/skills/ o .opencode/skills/ (Instalación de Skills base)     │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
             [Activación dinámica de Skills en el Ciclo SDD]
   ┌───────────────────────────────────────────────────────────────────┐
   │ • En Etapa 2 (Specify):   Skill de Notación EARS                  │
   │ • En Etapa 4 (Plan):      Skill de Modelado TypeSpec / OpenAPI    │
   │ • En Etapa 6 (Implement): Skill de TDD Estricto / local-dates     │
   │ • En Etapa 7 (Validate):  Skill de Contract Testing (Schemathesis)│
   └───────────────────────────────────────────────────────────────────┘
```

¿En qué etapa del flujo SDD deben ser creadas?

Las habilidades fundamentales del proyecto deben definirse o instalarse en la **Etapa 1: Constitución y Setup del Proyecto**, asegurando que el equipo cuente con las herramientas operativas antes de iniciar el ciclo. No obstante, al tratarse de módulos independientes, pueden añadirse nuevas skills de forma incremental en cualquier fase si el proyecto incorpora nuevas tecnologías o convenciones.

---

## **4\. Estructura y Ubicación en el Repositorio**

En **OpenCode** y el ecosistema estandarizado de agentes, las skills se alojan en ubicaciones jerárquicas bien definidas:

- **Nivel de Proyecto (Ámbito Local \- Recomendado):**
  - `.opencode/skills/<nombre-skill>/SKILL.md`
  - _(Permiten versionar las habilidades directamente en el repositorio Git del equipo)._
- **Nivel de Usuario / Global (Ámbito de Sistema):**
  - `~/.config/opencode/skills/<nombre-skill>/SKILL.md`
  - _(Disponibles para todos los proyectos ejecutados por el desarrollador en su máquina local)._
- **NOTA:** El **ID** de la Skill está determinado por el nombre en el path .opencode/skills/\<nombre-skill\>/SKILL.md donde el ID debe ser el \<nombre-skill\> usando minúsculas y separado por guiones (kebab-case).

---

## **5\. Elementos e Información Obligatoria de un `SKILL.md`**

Un archivo de habilidad optimizado debe estructurarse rigurosamente con las siguientes secciones:

1. **Metadatos Frontmatter (YAML Obligatorio):**
   1. **`name`:** Nombre para mostrar; por defecto, utiliza el ID derivado de la ruta, puede ser un nombre diferente al ID, aunque se recomienda el mismo ID en formato (Title Case) primera letra de cada palabra en mayúscula, cada palabra separada por un espacio.
   2. **`description`:** **El elemento más crítico.** Debe redactarse en lenguaje natural claro explicando qué resuelve la skill y en qué circunstancias exactas el agente debe activarla automáticamente es el resumen utilizado para mostrar la habilidad al modelo.
2. **Disparadores e Invocación (_Triggers_):** Lista explícita de palabras clave, comandos o tipos de archivo que provocan su activación.
3. **Flujo de Trabajo Paso a Paso:** Procedimiento determinista que la IA debe ejecutar para cumplir el objetivo.
4. **Reglas de Código y Patrones de Diseño:** Convenciones técnicas, sintaxis obligatoria y ejemplos concretos de buenas prácticas.
5. **Restricciones y Guardrails ("Qué NO hacer"):** Límites claros para prevenir malas prácticas o dependencias innecesarias.
6. **Comandos de Verificación:** Instrucciones para ejecutar pruebas automatizadas o linters asociados a la habilidad.

---

## **6\. Integración Operacional con OpenCode**

**OpenCode** cuenta con mecanismos nativos avanzados para descubrir, invocar y administrar **skills**:

- **Activación Autónoma e Implícita:** Si el usuario solicita: _"Agrega una prueba de contrato para el endpoint de tareas"_, OpenCode examina su catálogo, identifica que la descripción de la skill `contract-testing` coincide con la solicitud y carga automáticamente sus directivas.
- **Invocación Explícita mediante `@`:** El desarrollador puede forzar la activación inmediata de cualquier habilidad en el chat anteponiendo una arroba a su nombre (por ejemplo: `@local-dates Implementa el filtro de tareas por rango semanal`).
- **Instalación Directa desde Repositorios de la Comunidad:** OpenCode es compatible con el estándar universal de skills (`skills.sh`), permitiendo instalar paquetes oficiales y comunitarios con un solo comando:

```
npx skills add vercel-labs/agent-skills
```

---

## **7\. Plantilla Optimizada y Estandarizada (`SKILL.md`)**

````
# SKILL.md (Ejemplo base)

---
name: nombre-de-la-skill [ó Nombre De La Skill]
description: [Explicación detallada de la habilidad]. Úsala automáticamente siempre que el usuario pida [acción o tema] o al modificar archivos en [rutas o extensiones].
---

# Workflow: [Título corto del workflow autodescriptivo incluyendo el ID de la Skill]

## 1. Cuándo Invocarte (Triggers de Activación)
- Activa esta habilidad de forma automática cuando el usuario solicite:
  - [Caso de uso o palabra clave 1]
  - [Caso de uso o palabra clave 2]
- **No activar** si la solicitud está limitada a [excepciones o temas no cubiertos].

## 2. Contexto de Referencia y Gobernanza
Antes de aplicar las instrucciones, valida las restricciones generales en:
- `docs/constitution.md`
- `AGENTS.md`

## 3. Protocolo de Ejecución Paso a Paso
1. **Paso 1 (Inspección Previa):** Analizar los archivos involucrados y verificar [condición inicial].
2. **Paso 2 (Aplicación de Patrones):** Implementar la solución aplicando las siguientes reglas:
   - [Regla técnica A]
   - [Regla técnica B]
3. **Paso 3 (Verificación):** Confirmar el correcto funcionamiento ejecutando los comandos de validación.

## 4. Reglas Técnicas y Convenciones de Código
- **Estándar Obligatorio:** [Descripción de la convención técnica].
- **Patrón Prohibido:** [Descripción de lo que jamás debe hacerse].

## 5. Criterios de Aceptación y Pruebas
- Toda implementación debe estar respaldada por una prueba automatizada ejecutada con:
```bash
  [comando de prueba de la skill]
```
````

---

## **8\. Ejemplo Práctico: Skill `local-dates` para OpenCode**

A continuación se presenta un ejemplo real y completo del archivo **`.opencode/skills/local-dates/SKILL.md`** , diseñado para estandarizar la manipulación de fechas locales y almacenamiento UTC en un proyecto desarrollado con **OpenCode**:

````
# SKILL.md (Ejemplo base)

---
name: Local Dates
description: Úsala automáticamente siempre que escribas, modifiques o audites código que maneje fechas, marcas de tiempo (timestamps), horas, zonas horarias, cálculo de rachas diarias o filtros cronológicos.
---

# Workflow: Manejo Estandarizado de Fechas Locales (`local-dates`)

## 1. Cuándo Invocarte (Triggers)
- Activa esta habilidad ante solicitudes que involucren:
  - Cálculo de rachas de días consecutivos (*streaks*).
  - Filtros de tareas o eventos creados "hoy", "esta semana" o en rangos temporales.
  - Formateo de fechas para interfaces visuales o salida en consola CLI.
  - Persistencia o lectura de campos temporales en JSON, bases de datos o esquemas.

## 2. Principios de Gobernanza Temporal
1. **Almacenamiento Puro en UTC (ISO 8601):** Todo dato temporal almacenado en base de datos o serializado en JSON debe registrarse estrictamente en formato ISO 8601 en UTC con sufijo `Z` explícito (ej. `2026-11-12T15:30:00Z`).
2. **Presentación en Zona Horaria Local:** La conversión a la hora local del usuario debe ocurrir exclusivamente en la capa de presentación o interfaz (CLI / UI), nunca en el núcleo de dominio ni en los repositorios de persistencia.
3. **Cálculo de Días Calendario:** Para determinar si un evento ocurrió "hoy" o si una racha diaria se mantiene activa, el cálculo debe realizarse contra el día calendario local del usuario, no contra la fecha UTC del servidor.

## 3. Patrones de Código Aprobados (Python 3.12)

### Creación y Persistencia (Capa de Dominio y Repositorio)
```python
from datetime import datetime, timezone

# CORRECTO: Fecha aware en UTC para almacenamiento
def get_current_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
```

### Formateo para la Capa de Presentación (CLI)
```python
from datetime import datetime
from zoneinfo import ZoneInfo

# CORRECTO: Conversión a la zona local en la capa de salida
def format_for_display(utc_iso_string: str, user_tz_name: str = "America/Bogota") -> str:
    utc_dt = datetime.fromisoformat(utc_iso_string)
    local_dt = utc_dt.astimezone(ZoneInfo(user_tz_name))
    return local_dt.strftime("%d/%m/%Y %I:%M %p")
```

## 4. Prohibiciones Estrictas ("Qué NO hacer")

- PROHIBIDO: Usar datetime.now() o datetime.utcnow() sin especificar el parámetro timezone.utc (genera datetimes "ingenuos" o naive propensos a errores).
- PROHIBIDO: Almacenar marcas de tiempo en formato local o con cadenas formateadas arbitrariamente (ej. 12-11-2026 10:30).
- PROHIBIDO: Realizar comparaciones directas entre objetos datetime conscientes de zona horaria (aware) y objetos ingenuos (naive).

## 5. Verificación de Calidad
- Toda funcionalidad temporal debe contar con pruebas unitarias que simulen cambios de zona horaria y cruces de medianoche.
- Comando de verificación:

```bash
pytest tests/test_dates.py tests/test_streak_calculator.py -v
```
````

---
