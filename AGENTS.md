# Instrucciones del proyecto

## Alcance

- Este repositorio contiene scripts y configuraciones para ejecutar modelos LLM localmente con llama.cpp en Windows 11.
- `src/` contiene los scripts `.bat` de ejecución por modelo y sus configuraciones específicas; estos archivos sí forman parte del código versionable.
- `models/` contiene los modelos descargados, organizados en carpetas por modelo; los modelos no se versionan.
- `bin/` contiene dependencias y versiones precompiladas o compiladas de llama.cpp; sus artefactos locales no se versionan.
- `docs/` contiene el documento maestro de benchmarks y la documentación del flujo Git.
- `MEMORY.md` contiene el contexto operativo compacto para agentes.
- `CHANGELOG.md` registra los cambios del proyecto y sus releases.
- `main.bat`, cuando se cree, será el menú raíz para descubrir y ejecutar los scripts disponibles en `src/`.

## Regla no negociable: `llama.cpp/`

- `llama.cpp/` debe contener el repositorio oficial clonado desde GitHub.
- Los agentes no deben crear, modificar, eliminar, mover, renombrar ni sobrescribir ningún archivo o carpeta dentro de `llama.cpp/`.
- `llama.cpp/` solo puede consultarse para leer documentación y código de referencia de llama.cpp.
- `llama.cpp/` solo es necesario cuando se desea generar una versión compilada para la arquitectura de hardware local; no es necesario para ejecutar versiones precompiladas almacenadas en `bin/`.
- Antes de compilar localmente, clonar el repositorio oficial de llama.cpp en `llama.cpp/`.
- No generar nuevas compilaciones dentro de `llama.cpp/`, incluida cualquier carpeta `build/` existente.
- Las compilaciones, archivos temporales y resultados generados deben quedar fuera de `llama.cpp/`, preferiblemente dentro de una carpeta de salida excluida en `bin/`.
- Las instrucciones internas de `llama.cpp/` no autorizan a los agentes a modificar esa carpeta; la protección de este archivo tiene prioridad para el proyecto raíz.

## Estructura y archivos de soporte

- Los archivos `.gitkeep` conservan directorios estructurales en clones limpios, incluso cuando el contenido local de esas carpetas está excluido; no son scripts ni archivos de configuración funcionales.
- Los `.gitkeep` actuales son `bin/.gitkeep`, `models/.gitkeep` y `src/.gitkeep`; deben conservarse.
- `bin/deps/` contiene dependencias locales del entorno y `bin/llama-*` contiene versiones locales de llama.cpp.
- `LICENSE`, `README.md`, `MEMORY.md`, `AGENTS.md`, `CHANGELOG.md` y `.gitignore` pertenecen al proyecto raíz.
- El repositorio Git raíz todavía no está inicializado; aún no existen ramas, commits, tags ni releases.

## Ejecución local

- Los scripts deben funcionar desde cualquier directorio y construir sus rutas relativas a `%~dp0`; no depender del directorio actual desde el que se invoque el `.bat`.
- Usar rutas relativas a `bin`, `models` y `src` siempre que sea posible.
- Seleccionar explícitamente el ejecutable de llama.cpp y el archivo de modelo; no asumir que `llama.exe` o el modelo están en el `PATH`.
- Mantener separados los binarios precompilados de `bin/` y los artefactos generados al compilar llama.cpp.
- Antes de añadir una configuración nueva, comprobar que el ejecutable utilizado existe en la versión concreta de llama.cpp seleccionada.
- Verificar que el ejecutable y el modelo existan antes de iniciar una ejecución.

## Control de versiones

- Revisar `.gitignore` antes del primer commit y confirmar que `bin/`, `models/` y `llama.cpp/` están excluidos, mientras que los scripts de `src/` y los `.gitkeep` quedan versionables.
- No incorporar modelos, binarios, dependencias, controladores, firmware ni el contenido de `llama.cpp` al repositorio raíz.
- Seguir `docs/Flujo_de_Trabajo_Git.md` para ramas, integraciones, releases y tags.
- Registrar cambios relevantes en `CHANGELOG.md` bajo `Unreleased` hasta que exista un release.
- Los resultados permanentes de benchmark documentados pueden versionarse dentro de `docs/`; los resultados temporales deben guardarse en `logs/`, `results/` o `tmp/`, que están excluidos.
- Seguir la gramática de ramas y la estrategia de integración definidas en `docs/Flujo_de_Trabajo_Git.md`; no aplicar una estrategia alternativa.

## Restricciones de hardware

- La GPU objetivo es una NVIDIA RTX 5060 Ti con 16 GB de VRAM conectada por USB4; el desbordamiento hacia RAM puede reducir drásticamente el rendimiento.
- Usar `-ngl 99` como configuración inicial para descargar el máximo de capas a la GPU.
- Usar `-lm none` cuando el objetivo sea evitar el comportamiento de mmap documentado en las pruebas locales.
- Usar `-np 1` en modelos de 20B o más, salvo que una prueba específica demuestre que hay memoria suficiente para más slots.
- Los modelos de 10B-15B pueden probarse inicialmente con `-c 8192`; los modelos de 20B-24B requieren verificar el consumo real de VRAM antes de conservar ese contexto.
- Para modelos de 25B-28B, comenzar con `-c 4096`, `-np 1` y `-fa off` cuando pertenezcan a arquitecturas tipo Gemma.
- Para modelos de 30B-35B, comenzar con cuantización Q3, `-c 4096` y `-np 1`; tratarlos como ejecuciones analíticas o por lotes, no como configuraciones interactivas garantizadas.
- No declarar que un modelo está optimizado sin comprobar al menos carga, VRAM/RAM y velocidad con la configuración concreta.
