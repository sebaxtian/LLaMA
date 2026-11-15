# LLaMA

> Documento descriptivo de referencia no normativa. La norma suprema es `docs/constitution.md`; las reglas operativas están en `AGENTS.md` y la norma ejecutable del proceso en `docs/sdd/PROTOCOLO_OPERATIVO.md`. Este archivo describe el repositorio y su estado real; no fija reglas de obligado cumplimiento.

Entorno local para ejecutar y probar modelos de lenguaje (LLM) con [llama.cpp](https://github.com/ggml-org/llama.cpp) en Windows 11, sobre una eGPU NVIDIA RTX 5060 Ti.

El proyecto está orientado a:

- Programación avanzada en Python.
- Análisis de datos con Pandas y Matplotlib.
- Diseño y revisión de arquitectura de software.
- Ejecución local y privada de modelos LLM.
- Benchmarking de modelos bajo restricciones reales de VRAM y USB4.

## Metodología de desarrollo (SDD)

El proyecto se desarrolla con **Desarrollo Basado en Especificaciones (SDD)** en su variante **Spec-Anchored**. Toda feature, fix o cambio de configuración exige una especificación aprobada.

La base normativa vigente es la v2:

- **Rango 1:** `docs/constitution.md`.
- **Rango 2:** `AGENTS.md`.
- **Rango 3:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Rango 4:** `docs/Flujo_de_Trabajo_Git.md`.
- **Rango 5:** `docs/sdd/plantillas/`.
- **Rango 6:** `specs/NNN-slug/`.
- **Rango 7:** código de `src/`, `tools/`, `tests/` y `.opencode/`.

- **Ciclo:** Specify → Clarify → Plan → Tasks → Implement → Validate → Release.
- **Trazabilidad:** `RF/CB → CA → T → evidencia`.
- **Aprobaciones:** G1, G4 y G6 con commit firmado por el propietario; G2, G3 y G5 son verificaciones.
- **Validador:** `python tools\sdd\validate.py --all`. Comprueba estructura y alcance declarado; no acredita la firma de una aprobación ni la conformidad del régimen completo.

Las specs viven en `specs/NNN-slug/`. El corpus de referencia SDD está en `docs/sdd/`. Los agentes, comandos y skills de OpenCode están en `.opencode/`.

## Arquitectura

Hardware objetivo:

- **Equipo:** GEEKOM Mini IT13.
- **CPU:** Intel Core i9 de 13.ª generación.
- **RAM:** aproximadamente 32 GB.
- **GPU:** NVIDIA GeForce RTX 5060 Ti.
- **VRAM:** 16 GB GDDR6.
- **Conexión:** eGPU mediante USB4, hasta 40 Gbps.
- **Sistema operativo:** Windows 11.
- **Backend:** CUDA 13.5.

## Estructura del repositorio

```text
LLaMA/
├── AGENTS.md                           # Reglas operativas de rango 2
├── CHANGELOG.md                        # Registro de cambios y releases
├── LICENSE
├── MEMORY.md                           # Contexto operativo
├── README.md                           # Este documento descriptivo
├── example.env                         # Plantilla sin credenciales reales
├── main.bat                            # Menú principal de scripts
├── opencode.jsonc                      # Configuración de OpenCode y MCP
├── .opencode/                          # Agentes, comandos y skills
│   ├── agents/{sdd,planner,coder,reviewer,documenter}.md
│   ├── commands/sdd-*.md
│   └── skills/*/SKILL.md
├── bin/
│   ├── .gitkeep
│   ├── deps/                           # Dependencias locales, no versionadas
│   └── llama-master-bin-win-rtx5060ti-cuda-13.5-x64/
├── docs/
│   ├── constitution.md                 # Norma suprema de rango 1
│   ├── Flujo_de_Trabajo_Git.md         # Norma de rango 4
│   ├── Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md
│   └── sdd/
│       ├── PROTOCOLO_OPERATIVO.md      # Norma ejecutable de rango 3
│       ├── README.md                   # Índice del corpus y precedencia
│       ├── firmantes_autorizados       # Claves públicas de aprobación
│       ├── plantillas/                 # Contratos de rango 5
│       └── *.md                        # Corpus de referencia
├── specs/
│   ├── INDEX.md                        # Registro de especificaciones
│   └── NNN-slug/                       # Artefactos de cada spec
├── tools/
│   └── sdd/                            # Validador SDD y pruebas
├── llama.cpp/                          # Repositorio oficial local, no versionado
├── models/
│   ├── .gitkeep
│   └── gemma/                          # Modelos locales, no versionados
└── src/
    └── .gitkeep                        # Scripts de modelos, aún pendientes
```

`main.bat` existe y actúa como menú principal para seleccionar los scripts disponibles en `src/`. Los scripts de modelo todavía no se han creado.

### Responsabilidad de cada carpeta

- **`src/`**: scripts `.bat` con la configuración específica de cada modelo; se versionan.
- **`models/`**: modelos descargados, organizados por carpeta; no se versionan.
- **`bin/`**: dependencias y binarios locales; no se versionan.
- **`llama.cpp/`**: copia local del repositorio oficial para consulta y compilación; no se versiona.
- **`docs/`**: documentación técnica, normativa y de proceso.

Los archivos `.gitkeep` solo conservan los directorios estructurales en clones limpios.

## Inicio rápido

### 1. Comprobar los binarios

La versión precompilada disponible se encuentra en:

```text
bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64\
```

Los ejecutables principales son:

```text
llama-cli.exe       Ejecución interactiva
llama-server.exe    Servidor HTTP
llama-bench.exe     Benchmark
```

Para ejecutar una versión precompilada no es necesario clonar ni compilar `llama.cpp/`.

### 2. Colocar un modelo

Los modelos se organizan en `models/<nombre-del-modelo>/`. El repositorio contiene actualmente tres archivos `.gguf` bajo `models/gemma/`; no se versionan.

### 3. Crear un script de ejecución

Los scripts viven en `src/` y deben resolver la raíz con `%~dp0`. El siguiente ejemplo es ilustrativo; actualmente `src/` solo conserva `.gitkeep`.

```bat
@echo off
setlocal

set "ROOT=%~dp0.."
set "LLAMA_BIN=%ROOT%\bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64"
set "MODEL=%ROOT%\models\gemma\modelo.gguf"

if not exist "%LLAMA_BIN%\llama-cli.exe" (
    echo No se encontro llama-cli.exe
    pause
    exit /b 1
)

if not exist "%MODEL%" (
    echo No se encontro el modelo:
    echo %MODEL%
    pause
    exit /b 1
)

"%LLAMA_BIN%\llama-cli.exe" ^
    -m "%MODEL%" ^
    -ngl 99 ^
    -lm none ^
    -c 8192 ^
    -np 1

pause
```

### 4. Ejecutar

Desde la raíz del proyecto:

```bat
main.bat
```

## Configuración y resultados

Las configuraciones, benchmarks y límites de memoria están documentados en:

[Documento Maestro Consolidado](docs/Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md)

El flujo de ramas, releases y tags está documentado en:

[Flujo de Trabajo Git](docs/Flujo_de_Trabajo_Git.md)

Como referencia inicial, los scripts suelen utilizar:

```text
-ngl 99
-lm none
```

Los parámetros de contexto, slots y Flash Attention deben ajustarse según el modelo y su consumo de VRAM. Los modelos que excedan los 16 GB disponibles pueden utilizar RAM del sistema y sufrir una caída importante de rendimiento a través de USB4.

Los resultados de `llama-bench` no deben interpretarse automáticamente como rendimiento de un servidor con contexto largo.

## Estado actual

- Base normativa v2 publicada: constitución, `AGENTS.md`, protocolo operativo, flujo Git, plantillas, índice del corpus y lista de firmantes.
- Specs `SPEC-001` a `SPEC-008` integradas; `SPEC-009` en curso para la nueva base normativa.
- `main.bat` implementado como menú principal.
- Tres modelos `.gguf` locales bajo `models/gemma/`, excluidos de Git.
- Repositorio fuente oficial disponible en `llama.cpp/`, excluido de Git y protegido contra modificaciones.
- Pendiente de crear los scripts de modelos en `src/`.
- Las carpetas `logs/`, `results/` y `tmp/` están reservadas para resultados temporales locales.

## Archivos versionados y excluidos

| Se versiona | No se versiona |
|---|---|
| Documentación y reglas del proyecto | Modelos descargados |
| Scripts `.bat` dentro de `src/` | Binarios precompilados |
| `AGENTS.md`, `MEMORY.md` y `CHANGELOG.md` | Dependencias, instaladores y controladores |
| `README.md`, `LICENSE` y `.gitignore` | Contenido de `llama.cpp/` |
| `opencode.jsonc`, `example.env` | `.env`, `.vscode/` y credenciales locales |
| Documento maestro y flujo Git | Firmware y artefactos locales |
| `.gitkeep` de `bin/`, `models/` y `src/` | `logs/`, `results/`, `tmp/`, logs, temporales y dumps |

El repositorio raíz contiene documentación, configuración y scripts propios. Los artefactos externos deben obtenerse o prepararse localmente desde sus fuentes oficiales.

Los resultados permanentes de benchmark revisados y documentados pueden almacenarse en `docs/`. Los logs, dumps y resultados temporales deben guardarse en `logs/`, `results/` o `tmp/`, que están excluidos de Git.

## Configuración de OpenCode y GitHub MCP

La configuración del proyecto se encuentra en `opencode.jsonc`. El servidor remoto oficial de GitHub utiliza el nombre `github-mcp` y los toolsets `context`, `repos`, `issues` y `pull_requests`.

El token se obtiene desde la variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN`. `example.env` contiene únicamente una plantilla con un valor ficticio; las credenciales reales deben mantenerse en `.env`, excluido de Git y protegido contra lectura y edición por OpenCode.

Los servidores MCP nuevos deben utilizar nombres con el sufijo `-mcp`, y sus permisos o referencias de herramientas deben utilizar el nombre completo del servidor.

## Regla de protección de `llama.cpp/`

La carpeta `llama.cpp/` debe contener el repositorio oficial clonado desde GitHub. Ningún agente debe crear, modificar, eliminar, mover, renombrar ni sobrescribir archivos o carpetas dentro de ella.

Esta carpeta solo se utiliza para:

- Consultar la documentación y el código de referencia de llama.cpp.
- Generar versiones compiladas para una arquitectura de hardware local específica.

La copia de `llama.cpp/` no es necesaria para ejecutar versiones precompiladas disponibles en `bin/`. No deben generarse nuevas compilaciones dentro de `llama.cpp/`, incluida cualquier carpeta `build/`; las salidas deben guardarse fuera, preferiblemente en `bin/`.

## Licencia

La licencia MIT aplica al material propio del proyecto. `llama.cpp`, los modelos, binarios, CUDA, controladores, firmware y demás dependencias externas tienen licencias independientes y deben obtenerse desde sus fuentes oficiales.

La titularidad de `LICENSE` está confirmada: `Agent Sebaxtian` es la identidad legal definitiva, `agent@sebaxtian.dev` es el correo que se desea publicar y el titular posee los derechos del material propio incluido. La licencia MIT del proyecto no cubre componentes externos.
