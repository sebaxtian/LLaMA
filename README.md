# LLaMA

Entorno local para ejecutar y probar modelos de lenguaje (LLM) con
[llama.cpp](https://github.com/ggml-org/llama.cpp) en Windows 11, utilizando
una eGPU NVIDIA RTX 5060 Ti.

El proyecto está orientado principalmente a:

- Programación avanzada en Python.
- Análisis de datos con Pandas y Matplotlib.
- Diseño y revisión de arquitectura de software.
- Ejecución local y privada de modelos LLM.
- Benchmarking de modelos bajo restricciones reales de VRAM y USB4.

## Metodología de desarrollo (SDD)

El proyecto se desarrolla con **Desarrollo Basado en Especificaciones (SDD)** en su variante **Spec-Anchored**. Toda feature, fix o cambio de configuración exige una especificación aprobada.

- **Norma suprema:** `docs/constitution.md`.
- **Norma ejecutable:** `docs/sdd/PROTOCOLO_OPERATIVO.md`.
- **Reglas para agentes:** `AGENTS.md`.
- **Ciclo:** Specify → Clarify → Plan → Tasks → Implement (TDD) → Validate.
- **Trazabilidad:** `RF/CB → CA → T → evidencia → commit → merge → release`.
- **Validador:** `python tools\sdd\validate.py --all`.

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

La estructura actual del proyecto es:

```text
LLaMA/
├── .gitignore
├── AGENTS.md                           # Reglas operativas para agentes
├── CHANGELOG.md
├── example.env                         # Plantilla sin credenciales reales
├── LICENSE
├── MEMORY.md
├── opencode.jsonc                      # Configuración de OpenCode y MCP
├── README.md
├── .opencode/                          # Agentes, comandos y skills
│   ├── agents/{sdd,planner,coder,reviewer}.md
│   ├── commands/sdd-*.md
│   └── skills/*/SKILL.md
├── bin/
│   ├── .gitkeep                       # Conserva la carpeta estructural
│   ├── deps/                          # Dependencias locales, no versionadas
│   └── llama-master-bin-win-rtx5060ti-cuda-13.5-x64/
│                                      # Binarios locales, no versionados
├── docs/
│   ├── constitution.md                 # Norma suprema del proyecto
│   ├── Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md
│   ├── Flujo_de_Trabajo_Git.md
│   └── sdd/                            # Corpus y protocolo SDD
├── specs/
│   └── INDEX.md                        # Registro de especificaciones
├── tools/
│   └── sdd/                            # Validador SDD y pruebas
├── llama.cpp/                         # Repositorio oficial local, no versionado
├── models/
│   └── .gitkeep                       # Conserva la carpeta estructural
└── src/
    └── .gitkeep                       # Conserva la carpeta estructural
```

`main.bat` todavía no existe. Cuando se implemente, será el menú principal para seleccionar los scripts disponibles en `src/`.

### Responsabilidad de cada carpeta

- **`src/`**: scripts `.bat` con la configuración específica de cada modelo; estos archivos sí se versionan.
- **`models/`**: modelos descargados, organizados en carpetas individuales; los modelos no se versionan.
- **`bin/`**: dependencias y binarios locales; no se versionan.
- **`llama.cpp/`**: copia local del repositorio oficial para consulta y compilación; no se versiona desde el repositorio raíz.
- **`docs/`**: resultados de pruebas y documentación técnica.

Los archivos `.gitkeep` solo conservan los directorios estructurales en clones limpios. No son scripts ni archivos de configuración funcionales.

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

Los resultados permanentes de benchmark que hayan sido revisados y documentados pueden almacenarse en `docs/`. Los logs, dumps y resultados temporales deben guardarse en `logs/`, `results/` o `tmp/`, que están excluidos de Git.

La licencia MIT aplica al material propio del proyecto. `llama.cpp`, los modelos, binarios, CUDA, controladores, firmware y demás dependencias externas tienen licencias independientes y deben obtenerse desde sus fuentes oficiales.

La titularidad de `LICENSE` está confirmada: `Agent Sebaxtian` es la identidad legal definitiva, `agent@sebaxtian.dev` es el correo que se desea publicar y el titular posee los derechos del material propio incluido. La licencia MIT del proyecto no cubre componentes externos.

## Configuración de OpenCode y GitHub MCP

La configuración del proyecto se encuentra en `opencode.jsonc`. El servidor remoto oficial de GitHub utiliza el nombre `github-mcp` y los toolsets `context`, `repos`, `issues` y `pull_requests`.

El token se obtiene desde la variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN`. `example.env` contiene únicamente una plantilla con un valor ficticio; las credenciales reales deben mantenerse en `.env`, que está excluido de Git y protegido contra lectura y edición por OpenCode.

Los servidores MCP nuevos deben utilizar nombres con el sufijo `-mcp`, y sus permisos o referencias de herramientas deben utilizar el nombre completo del servidor.

## Regla de protección de `llama.cpp/`

La carpeta `llama.cpp/` debe contener el repositorio oficial clonado desde GitHub. Ningún agente debe crear, modificar, eliminar, mover, renombrar ni sobrescribir archivos o carpetas dentro de ella.

Esta carpeta solo se utiliza para:

- Consultar la documentación y el código de referencia de llama.cpp.
- Generar versiones compiladas para una arquitectura de hardware local específica.

La copia de `llama.cpp/` no es necesaria para ejecutar versiones precompiladas disponibles en `bin/`. No deben generarse nuevas compilaciones dentro de `llama.cpp/`, incluida cualquier carpeta `build/`; las salidas deben guardarse fuera, preferiblemente en `bin/`.

## Flujo de trabajo

### Usar una versión precompilada

1. Descargar una versión precompilada de llama.cpp desde sus releases oficiales.
2. Guardarla dentro de una carpeta `bin/llama-*`.
3. Descargar el modelo en formato GGUF.
4. Crear una carpeta para el modelo dentro de `models/`.
5. Crear un script `.bat` dentro de `src/`.
6. Configurar el ejecutable, el modelo y los parámetros de inferencia.
7. Probar la ejecución y registrar los resultados en el documento maestro.

### Compilar para el hardware local

1. Clonar el repositorio oficial de llama.cpp en la carpeta `llama.cpp/`.
2. Consultar allí la documentación de compilación correspondiente a Windows y CUDA.
3. Generar los artefactos de compilación fuera de `llama.cpp/`.
4. Guardar la versión resultante dentro de `bin/llama-*`.
5. Continuar con la descarga del modelo y la creación del script en `src/`.

Cada script debe utilizar rutas relativas al proyecto mediante `%~dp0` y no depender del directorio desde el que se invoque.

## Inicio rápido

### 1. Comprobar los binarios

La versión precompilada actualmente disponible se encuentra en:

```text
bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64\
```

Los ejecutables principales son:

```text
llama-cli.exe       Ejecución interactiva
llama-server.exe    Servidor HTTP
llama-bench.exe     Benchmark
```

Para ejecutar una versión precompilada no es necesario clonar ni compilar el repositorio `llama.cpp/`.

### 2. Colocar un modelo

Crear una carpeta para el modelo:

```text
models\<nombre-del-modelo>\
```

Guardar dentro el archivo `.gguf`, por ejemplo:

```text
models\phi-4\phi-4-Q6_K.gguf
```

### 3. Crear un script de ejecución

Crear un archivo dentro de `src/`, por ejemplo:

```text
src\phi-4.bat
```

El ejemplo siguiente es ilustrativo; actualmente no existe `src\phi-4.bat` ni el modelo de ejemplo.

```bat
@echo off
setlocal

set "ROOT=%~dp0.."
set "LLAMA_BIN=%ROOT%\bin\llama-master-bin-win-rtx5060ti-cuda-13.5-x64"
set "MODEL=%ROOT%\models\phi-4\phi-4-Q6_K.gguf"

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

### 4. Ejecutar el modelo

Desde la raíz del proyecto:

```bat
src\phi-4.bat
```

Cuando `main.bat` esté implementado, será posible seleccionar el modelo desde un menú centralizado:

```bat
main.bat
```

## Configuración y resultados

Las configuraciones, benchmarks y límites de memoria de la arquitectura están documentados en:

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

- Estructura base del proyecto creada.
- Repositorio Git raíz inicializado.
- Existen las ramas `main`, `dev` y la rama de trabajo documentada en `docs/Flujo_de_Trabajo_Git.md`.
- Metodología SDD configurada: constitución, protocolo operativo, corpus, validador, agentes, comandos y skills.
- Archivos `.gitkeep` presentes para conservar `bin/`, `models/` y `src/` inicializadas.
- Dependencias y binarios precompilados disponibles localmente en `bin/`, excluidos de Git.
- Repositorio fuente oficial disponible en `llama.cpp/`, excluido de Git y protegido contra modificaciones.
- Documentación de benchmarks y flujo Git disponible en `docs/`.
- Pendiente de crear los scripts de modelos en `src/`.
- Pendiente de descargar y organizar modelos en `models/`.
- Pendiente de implementar el menú `main.bat` (piloto `SPEC-001`).
- Las carpetas `logs/`, `results/` y `tmp/` están reservadas para resultados temporales locales.
