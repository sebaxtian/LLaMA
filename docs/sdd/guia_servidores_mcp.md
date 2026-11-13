# **Guía Integral: Definición, Configuración e Integración de Servidores MCP (Model Context Protocol)**

> **Documento de referencia (no normativo).** Ante contradicción prevalece `PROTOCOLO_OPERATIVO.md`, y por encima `AGENTS.md` y `docs/constitution.md`.

El **Model Context Protocol (MCP)** es un estándar abierto e interfaz universal impulsada por la industria (creada inicialmente por Anthropic y adoptada ampliamente por plataformas agénticas como **OpenCode**, Claude Code, Cursor, VS Code y OpenAI Codex) que permite conectar a los agentes de Inteligencia Artificial con herramientas externas, bases de datos, APIs y entornos de ejecución en tiempo real de forma segura y estructurada.

En el desarrollo asistido por IA, los servidores MCP actúan como un **puerto de extensión universal**: en lugar de que el modelo trabaje aislado dependiendo únicamente de su entrenamiento estático o de fragmentos de código copiados manualmente, el protocolo le permite interactuar directamente con el entorno operativo y fuentes dinámicas de datos.

---

## **1\. Fundamentos y Casos de Uso Principales**

El protocolo MCP resuelve el aislamiento de contexto y la desactualización de información mediante cuatro capacidades clave:

1. **Inyección de Documentación Técnica en Tiempo Real:** Conexión con servicios especializados como **Context7** para consultar documentación oficial y actualizada de frameworks (Next.js, Tailwind, Supabase, etc.), evitando que el agente genere código con sintaxis obsoleta o métodos deprecados.
2. **Acceso Seguro a Bases de Datos:** Permite al agente inspeccionar esquemas, consultar tablas o validar migraciones en bases de datos locales o remotas (PostgreSQL, SQLite, Supabase) sin exponer credenciales en el historial de chat.
3. **Automatización y Pruebas en Navegadores Reales:** Integración con servidores MCP de automatización web (como **Chrome DevTools** o **Playwright**) para que el agente abra navegadores, interactúe con la interfaz de usuario, detecte errores en la consola y capture evidencias visuales.
4. **Sincronización con Herramientas Empresariales:** Conexión directa con plataformas como GitHub, Jira, Confluence o Figma para leer especificaciones, issues o esquemas de diseño directamente dentro del flujo de trabajo.

---

## **2\. Rol en la Metodología de Desarrollo Basado en Especificaciones (SDD)**

Dentro del flujo de **Desarrollo Basado en Especificaciones (SDD, _Spec-Driven Development_)**, los servidores MCP actúan como el arnés de contexto extendido que alimenta varias de sus etapas clave:

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 1: CONSTITUCIÓN / SETUP                       │
 │  • Declaración de MCPs en opencode.json (Context7, DevTools, DBs)       │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                  ETAPA 4: PLANIFICACIÓN TÉCNICA (Plan)                  │
 │  • Uso de MCP de Documentación (Context7) para validar APIs y esquemas  │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   ETAPA 6: IMPLEMENTACIÓN (Implement)                   │
 │  • Consultas a BD y herramientas de compilación asistidas por MCP       │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
                                      ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                     ETAPA 7: VALIDACIÓN (Validate)                      │
 │  • Uso de MCP de Navegador (Playwright/Chrome) para verificar criterios │
 │    EARS visuales y asegurar la convergencia del contrato                │
 └─────────────────────────────────────────────────────────────────────────┘
```

- **En la Fase de Planificación (`plan.md`):** Garantiza que las firmas de interfaces, esquemas y dependencias seleccionadas se diseñen con base en la documentación oficial más reciente.
- **En la Fase de Validación (`Validate`):** Permite que el subagente de auditoría ejecute pruebas end-to-end automáticas mediante un MCP de navegador, confirmando que la interfaz cumple los criterios de aceptación EARS y no arroja errores de renderizado.
- **Momento de Configuración:** Se configuran principalmente en la **Etapa 1 (Setup del Proyecto)** en el archivo de configuración del entorno (`opencode.jsonc`), aunque pueden registrarse servidores adicionales si una funcionalidad específica lo requiere.

---

## **3\. Tipos de Transporte y Estructura Técnica**

Un servidor MCP se define de forma declarativa en formato **JSON**. En herramientas como **OpenCode**, se aloja en el archivo de configuración en la raíz del proyecto (`opencode.jsonc`) o en la configuración global del sistema operativo (`~/.config/opencode/config.jsonc`).

El estándar contempla dos mecanismos principales de transporte:

1. **Transporte Local (`local`):** Ejecuta un proceso o script local directamente en la máquina anfitriona (usualmente mediante `npx`, `python`, `node` o un binario del sistema), comunicándose a través de la entrada y salida estándar.
2. **Transporte Remoto (`remote`):** Establece una conexión en red con un servidor externo mediante _Server-Sent Events_ (SSE) o llamadas HTTP autenticadas a través de una URL.

### **Elementos Obligatorios que debe Contener:**

- **Identificador del Servidor:** Nombre único para el MCP (ej. `context7-mcp`, `chrome-devtools-mcp`, `postgres-mcp`, `github-mcp`).
- **Tipo de Transporte (`type` / `transport`):** Declaración explícita de `local` o `remote`.
- **Comando y Argumentos (`command` y `args`):** Para transportes locales, especifica el ejecutable y sus banderas.
- **URL (`url`):** Para transportes remotos, define el endpoint de red.
- **Variables de Entorno y Encabezados (`env` / `oauth` / `headers`):** Claves de API, credenciales de conexión o tokens de autenticación requeridos para operar.

---

## **4\. Integración Operacional con OpenCode**

**OpenCode** cuenta con gestión nativa para el ciclo de vida de los servidores MCP:

- **Gestor Interactivo en la TUI (`/mcps`):** Al escribir `/mcps` en la consola de OpenCode, se despliega una lista interactiva de todos los servidores registrados. Puedes activar (`enable`) o desactivar (`disable`) servidores presionando la barra espaciadora para ahorrar tokens y mantener la ventana de contexto despejada.
- **Comandos de Consola (CLI):**
  - `opencode mcp list`: Lista todos los servidores MCP configurados en el proyecto y su estado.
  - `opencode mcp add`: Inicia un asistente interactivo en la terminal para vincular un servidor nuevo.
  - `opencode mcp auth <nombre-mcp>`: Ejecuta el flujo de autenticación para servidores remotos que requieren credenciales.
- **Invocación Autónoma o Dirigida:** OpenCode identifica cuándo una consulta necesita de las herramientas provistas por un MCP activo y lo utiliza automáticamente. También se puede forzar su uso explícito en el prompt: _"Consulta la documentación de Tailwind v4 usando el MCP de context7-mcp"_.

---

## **5\. Plantilla Optimizada y Estandarizada (`opencode.jsonc`)**

A continuación se muestra la plantilla estándar para configurar servidores MCP tanto locales como remotos en la raíz de tu proyecto:

```
{
  // opencode.jsonc (Ejemplo base)

  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "nombre-mcp-remoto": {
        "type": "remote",
        "url": "[suspicious link removed]",
        "headers": {
          "Authorization": "Bearer {env:TU_API_KEY_AQUI}",
        },
       "nombre-mcp-local": {
        "type": "local",
        "command": "npx",
        "args": [
          "-y",
          "@organizacion/servidor-mcp@latest"
        ],
        "env": {
          "SECRECT_TOKEN": "{env:SECRECT_TOKEN}",
        },
       },
      },
    },
  },
}
```

---

## **6\. Ejemplo Práctico: Configuración de Context7 y Chrome DevTools en OpenCode**

Ejemplo real de un archivo `opencode.jsonc` configurado para combinar documentación técnica remota (**Context7**) y automatización de pruebas web local (**Chrome DevTools**):

```
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "context7-mcp": {
        "type": "remote",
        "url": "[suspicious link removed]",
        "headers": {
          "Authorization": "Bearer {env:TU_API_KEY_AQUI}"
        }
      },
      "chrome-devtools-mcp": {
        "type": "local",
        "command": "npx",
        "args": [
          "-y",
          "@chrome/devtools-mcp@latest"
        ]
      }
    }
  }
}
```

**Flujo de Interacción en la Terminal de OpenCode:**

```
> /mcps
  [x] context7 (Enabled)
  [x] chrome-devtools (Enabled)

> Prompt: "Diseña el componente de exportación de datos en React.
  1. Usa el MCP de context7-mcp para consultar la documentación oficial de la última versión de @tanstack/react-table.
  2. Implementa el componente en src/components/ExportTable.tsx.
  3. Usa el MCP de chrome-devtools-mcp para abrir http://localhost:3000/export y verificar que la tabla renderice sin errores en la consola del navegador."
```

---
