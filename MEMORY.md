# Memoria operativa del proyecto LLaMA

## Identidad y estado

- Proyecto: `LLaMA`.
- Objetivo: ejecutar, probar y comparar modelos LLM localmente mediante llama.cpp.
- Plataforma: Windows 11.
- Caso de uso principal: programación en Python, análisis de datos y arquitectura de software.
- El repositorio Git raíz está inicializado. `main` y `dev` existen; las ramas de trabajo, tags y releases se documentan según el estado actual de `docs/Flujo_de_Trabajo_Git.md`.

## Hardware objetivo

- Equipo: GEEKOM Mini IT13.
- CPU: Intel Core i9 de 13.ª generación.
- RAM: aproximadamente 32 GB.
- GPU: NVIDIA RTX 5060 Ti.
- VRAM: 16 GB GDDR6.
- Conexión: eGPU mediante USB4.
- Backend: CUDA 13.5.

## Mapa operativo

- `src/`: scripts `.bat` de ejecución por modelo; estos scripts sí deben versionarse.
- `models/`: modelos descargados; actualmente contiene solo `.gitkeep` y los modelos no se versionan.
- `bin/deps/`: dependencias locales excluidas de Git.
- `bin/llama-*`: versiones precompiladas o compiladas de llama.cpp, excluidas de Git.
- `docs/`: documento maestro de benchmarks y flujo de trabajo Git.
- `llama.cpp/`: repositorio oficial para consulta y compilación local; nunca modificarlo.
- `AGENTS.md`: reglas obligatorias para agentes.
- `README.md`: guía general del proyecto.
- `CHANGELOG.md`: historial de cambios y releases.
- `opencode.jsonc`: configuración de OpenCode, permisos y servidores MCP.
- `example.env`: plantilla versionable para variables de entorno sin credenciales reales.
- `.env`: variables locales ignoradas y protegidas contra lectura y edición por OpenCode.
- `.vscode/`: configuración local del editor, excluida del repositorio.
- `.gitkeep`: conserva `bin/`, `models/` y `src/` en clones limpios.
- `main.bat`: pendiente de implementación; será el menú principal.
- `logs/`, `results/` y `tmp/`: resultados temporales y archivos locales excluidos.

## Regla crítica sobre `llama.cpp/`

Nunca crear, modificar, eliminar, mover, renombrar o sobrescribir archivos o carpetas dentro de `llama.cpp/`.

La carpeta `llama.cpp/` solo debe utilizarse para:

1. Consultar documentación y código de referencia.
2. Generar compilaciones para el hardware local específico.

Antes de compilar localmente, el repositorio oficial debe estar clonado en `llama.cpp/`. No generar nuevas salidas dentro de esa carpeta, incluida cualquier carpeta `build/`; los artefactos deben quedar fuera, preferiblemente en `bin/`.

Para ejecutar versiones precompiladas no es necesario clonar ni compilar `llama.cpp/`.

## Reglas de ejecución

- Los `.bat` deben resolver la raíz mediante `%~dp0`.
- No depender del directorio actual ni del `PATH` del sistema.
- Seleccionar explícitamente el ejecutable y el archivo `.gguf`.
- Verificar que existan el ejecutable y el modelo antes de iniciar.
- No colocar modelos dentro de `bin/`.
- No colocar binarios dentro de `models/`.
- No eliminar ni modificar `.gitkeep` mientras las carpetas correspondientes deban permanecer inicializadas.

## Parámetros iniciales

- GPU offload: `-ngl 99`.
- Carga del modelo: `-lm none`.
- Modelos de 20B o más: comenzar con `-np 1`.
- Modelos de 10B-15B: probar inicialmente con `-c 8192`.
- Modelos de 20B-24B: validar VRAM antes de usar contextos largos.
- Modelos de 25B-28B: comenzar con `-c 4096 -np 1`.
- Arquitecturas tipo Gemma: comenzar con `-fa off`.
- Modelos de 30B-35B: usar cuantización Q3, `-c 4096` y `-np 1`.

## Criterios de validación

Antes de considerar funcional u optimizado un script, comprobar:

- Que el ejecutable exista.
- Que el modelo exista.
- Que la configuración corresponda al modelo.
- Consumo de VRAM y RAM.
- Tokens por segundo.
- Si existe desbordamiento hacia memoria compartida.
- Versión concreta de llama.cpp utilizada.

No asumir que el resultado de `llama-bench` representa el rendimiento de un servidor con contexto largo.

## Preparación Git y flujo de trabajo

Antes del primer commit:

1. Revisar `.gitignore`.
2. Confirmar que `bin/`, `models/` y `llama.cpp/` están excluidos.
3. Confirmar que `bin/.gitkeep`, `models/.gitkeep` y `src/.gitkeep` se conservan.
4. Confirmar que los futuros scripts de `src/` son versionables.

El flujo de ramas, releases y tags está definido en `docs/Flujo_de_Trabajo_Git.md`.

La política vigente es determinista: merge `--no-ff`, sin rebase ni squash; ramas con nombres `feat/*`, `fix/*` o `hotfix/*` usando minúsculas, números y guiones; tags anotados `vMAJOR.MINOR.PATCH` con mensaje `Release vX.Y.Z`; primera versión funcional `v0.1.0`.

`main` y `dev` son ramas protegidas por política. Los conflictos de features y fixes se resuelven en sus ramas de trabajo; los conflictos de sincronización de un hotfix se resuelven en `hotfix/*` o `dev` según el merge definido en `docs/Flujo_de_Trabajo_Git.md`.

## Convención de nombres MCP

Los servidores MCP configurados en OpenCode deben utilizar nombres con el sufijo `-mcp`, por ejemplo `github-mcp`. Esta convención también debe utilizarse al definir permisos o referencias a sus herramientas.

## Referencias principales

- `docs/Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md`
- `docs/Flujo_de_Trabajo_Git.md`
