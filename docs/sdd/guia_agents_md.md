# **Guía Integral: Definición, Gobernanza e Integración de `AGENTS.md`**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

`AGENTS.md` es un estándar abierto, determinista y ligero diseñado para actuar como la **guía contextual de entrada (_System Prompt_ de repositorio)** para los agentes de Inteligencia Artificial que inspeccionan, refactorizan o generan código dentro de un proyecto.

A diferencia del archivo `README.md` convencional —orientado a la incorporación de desarrolladores humanos mediante tutoriales de instalación o notas de lanzamiento—, `AGENTS.md` está estrictamente optimizado para ser procesado por **agentes de codificación con IA** (tales como OpenCode, Claude Code, OpenAI Codex, Cursor, Aider y GitHub Copilot).

---

## **1\. Fundamentos y Propósito de `AGENTS.md`**

El archivo `AGENTS.md` resuelve tres desafíos críticos en el desarrollo de software asistido por Inteligencia Artificial:

1. **Persistencia de Contexto sin Repetición:** Evita que el equipo deba repetir manualmente en cada sesión o _prompt_ las directrices del proyecto (versiones de lenguaje, bibliotecas permitidas, estructura de directorios o normas de pruebas).
2. **Optimización de Tokens y Ventana de Contexto:** Impide que los agentes consuman de forma ineficiente miles de tokens explorando heurísticamente el repositorio completo en cada arranque para deducir las convenciones del código.
3. **Límites de Seguridad y Gobernanza (_Guardrails_):** Declara explícitamente qué acciones, dependencias o modificaciones están prohibidas, previniendo alucinaciones y la acumulación de deuda técnica.

---

## **2\. Rol en la Metodología de Desarrollo Basado en Especificaciones (SDD)**

Dentro del flujo de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**, `AGENTS.md` se ubica en la capa de **Constitución y Arneses Operativos (_Setup / Harnessing_)**.

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

- **Relación con `constitution.md`:** Mientras que la Constitución define los principios innegociables y la visión del producto a nivel institucional, `AGENTS.md` traduce esas reglas a un plano puramente operacional: comandos concretos de terminal, verificaciones de linters y reglas de ejecución para los agentes.
- **Momento de Creación:** Debe definirse de forma obligatoria en la **Etapa 1 (Setup del Proyecto)**, antes de iniciar la redacción de especificaciones funcionales (`spec.md`) o planes de ingeniería (`plan.md`).

---

## **3\. Principios de Diseño y Estructura Técnica**

Para mantener la efectividad del agente sin desbordar su contexto, `AGENTS.md` debe seguir tres criterios fundamentales:

- **Ubicación en el Repositorio:** Se sitúa en la raíz del proyecto (`/AGENTS.md`). En arquitecturas monorrepo complejas, pueden añadirse archivos `AGENTS.md` anidados en subdirectorios; el agente otorgará prioridad al archivo más cercano a los módulos que esté editando.
- **Concisión y Densidad de Información:** Debe mantenerse condensado (idealmente entre 30 y 70 líneas útiles). NOTA: No debe contener tutoriales extensos ni documentación teórica, sino directrices verificables.
- **Formulación Directa y Verificable:** Las instrucciones deben formularse en modo afirmativo o imperativo, indicando comandos exactos y rutas de directorios absolutas dentro del árbol del proyecto.

### **Elementos Obligatorios que debe Contener:**

1. **Misión del Proyecto:** Resumen de 1 a 2 oraciones sobre el propósito del sistema.
2. **Stack Tecnológico y Restricciones:** Versión exacta del runtime, motor de persistencia y dependencias autorizadas.
3. **Comandos Principales del Entorno:** Comandos exactos para instalar dependencias, ejecutar pruebas unitarias, lanzar linters y verificar tipos.
4. **Mapa de Estructura del Repositorio:** Rutas clave para lógica de dominio, adaptadores, pruebas y especificaciones.
5. **Convenciones de Código y Estilo:** Pautas de formateo, tipado estricto e idioma de los componentes.
6. **Límites Operativos ("Qué NO hacer"):** Lista explícita de patrones no autorizados, archivos protegidos y prohibiciones.
7. **Puntos de Referencia a Especificaciones:** Enlace directo a las especificaciones activas y al documento constitucional.

---

## **4\. Integración Operacional con OpenCode**

**OpenCode** incorpora soporte nativo para el estándar `AGENTS.md` a través de los siguientes mecanismos de ejecución:

- **Lectura Automática en el Arranque:** Al ejecutar `opencode` en la terminal, el agente lee automáticamente el archivo `AGENTS.md` de la raíz del espacio de trabajo y lo inyecta como contexto base de la sesión.
- **Inicialización Asistida (`/init`):** Si se ejecuta el comando `/init` dentro de **OpenCode** en un proyecto nuevo o existente, el agente analiza la estructura de directorios y genera automáticamente un borrador base de `AGENTS.md`.
- **Coordinación con Skills y MCPs:** `AGENTS.md` sirve como el índice principal que indica al agente cuándo debe invocar servidores MCP (como Context7 para documentación) o cargar habilidades procedimentales (`.opencode/skills/`).

---

## **5\. Plantilla Optimizada y Estandarizada (`AGENTS.md`)**

```
# AGENTS.md (Ejemplo base)

## Misión del Proyecto
[1 a 2 oraciones describiendo la finalidad del software y los usuarios o sistemas principales].

## Stack Tecnológico y Restricciones
- **Lenguaje / Runtime:** [ej. Python 3.12 / TypeScript 5.x]
- **Tipado:** [Estricto / mypy --strict / tsconfig strict]
- **Persistencia:** [ej. PostgreSQL 16 vía Prisma / Archivo JSON local]
- **Dependencias:** Uso exclusivo de librerías autorizadas en [pyproject.toml / package.json]. Prohibida la instalación de dependencias no aprobadas.

## Comandos Principales de Ejecución
- **Instalar dependencias:** `[comando exacto]`
- **Servidor de desarrollo:** `[comando exacto]`
- **Ejecución de pruebas:** `[comando exacto]`
- **Linter y formateador:** `[comando exacto]`
- **Chequeo de tipos estáticos:** `[comando exacto]`

## Estructura del Repositorio
- `src/core/`: Lógica de dominio pura y reglas de cálculo (sin dependencias de I/O).
- `src/adapters/`: Interfaces de entrada/salida, bases de datos y controladores.
- `tests/`: Suites de pruebas automatizadas unitarias y de integración.
- `specs/`: Especificaciones funcionales, planes y tareas SDD.

## Convenciones de Código y Calidad
- Funciones y métodos con firmas de tipo explícitas en parámetros y retornos.
- Formato de commits: seguir la convención `[modulo] <tipo>: <descripcion breve>`.
- Todo cambio en la lógica de negocio requiere su respectiva prueba automatizada.

## Prohibiciones y Límites ("Qué NO hacer")
- NO modificar esquemas de base de datos ni contratos de interfaz sin actualizar la especificación primero.
- NO introducir frameworks pesados ni dependencias externas sin autorización previa.
- NO marcar tareas como finalizadas si las pruebas automatizadas no reportan 100% de éxito.

## Flujo SDD y Documentación
- Consultar obligatoriamente `docs/constitution.md` antes de proponer cambios arquitectónicos.
- La especificación activa de cada funcionalidad se encuentra en `specs/<id-feature>/spec.md`.
- Fuerte en determinismo Git (docs/Flujo_de_Trabajo_Git.md)
```

---

## **6\. Ejemplo Práctico: CLI TaskTracker en Python con OpenCode**

A continuación se presenta un **ejemplo** real del archivo `AGENTS.md` configurado para un proyecto de consola desarrollado en Python con OpenCode:

```
# AGENTS.md (Ejemplo base)

## Misión del Proyecto
Herramienta CLI ligera en Python para el seguimiento de tareas personales orientada a desarrolladores, con almacenamiento local determinista y bajo consumo de recursos.

## Stack Tecnológico y Restricciones
- Python 3.12 utilizando el sistema de tipos estricto (`mypy --strict`).
- Persistencia exclusiva en archivo JSON local (`~/.tasks.json`).
- Prohibido el uso de ORMs pesados o frameworks externos de línea de comandos (usar `argparse` nativo).
- Suite de pruebas gestionada exclusivamente con `pytest`.

## Comandos Principales de Ejecución
- **Entorno virtual:** `source venv/bin/activate`
- **Instalar dependencias de desarrollo:** `pip install -e ".[dev]"`
- **Ejecutar suite de pruebas:** `pytest tests/ -v`
- **Verificación de tipos estáticos:** `mypy src/ tests/`
- **Linter y formato de código:** `ruff check src/ && ruff format --check src/`

## Estructura del Repositorio
- `src/domain.py`: Entidades puras de tareas y lógica de validación de negocio.
- `src/repository.py`: Adaptador de lectura y escritura para el archivo JSON.
- `src/cli.py`: Analizador de argumentos de consola y formateador de salida estándar.
- `tests/`: Pruebas unitarias de dominio y pruebas de integración sobre archivos temporales.
- `specs/`: Contiene los incrementos SDD (`spec.md`, `plan.md`, `tasks.md`).

## Convenciones de Código y Calidad
- Nombres de funciones, variables y pruebas redactados en inglés técnico.
- Mensajes de error en consola dirigidos al usuario redactados en español.
- Ninguna función pública puede carecer de anotaciones de tipos completas.

## Prohibiciones y Límites
- NO utilizar llamadas directas a `sys.exit()` dentro de `domain.py` ni de `repository.py`.
- NO realizar mutaciones sobre la base de datos o almacenamiento sin validar previamente el formato ISO 8601 en fechas.
- NO omitir la ejecución de `pytest` antes de reportar una tarea como completada.

## Flujo de Trabajo y Especificaciones
- Leer `docs/constitution.md` para verificar los principios innegociables del proyecto.
- Trabajar siempre sobre la tarea activa indicada en `specs/NNN-slug/tasks.md`.
- Fuerte en determinismo Git (docs/Flujo_de_Trabajo_Git.md)
```

---
