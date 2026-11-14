# Memoria operativa del proyecto LLaMA

> Documento descriptivo de referencia no normativa. La norma suprema es `docs/constitution.md`; las reglas operativas están en `AGENTS.md` y la norma ejecutable en `docs/sdd/PROTOCOLO_OPERATIVO.md`. Este archivo resume el contexto operativo y no fija reglas.

## 1. Identidad y estado

- Proyecto: `LLaMA`.
- Objetivo: ejecutar, probar y comparar modelos LLM localmente mediante llama.cpp.
- Plataforma: Windows 11.
- Caso de uso principal: programación en Python, análisis de datos y arquitectura de software.
- Base normativa vigente: v2, con constitución, `AGENTS.md`, protocolo operativo, flujo Git, plantillas e índice del corpus.
- Repositorio Git inicializado. `main` y `dev` protegidas; todo cambio entra por Pull Request con `merge --no-ff`.
- Estado de specs: `SPEC-001` a `SPEC-008` integradas; `SPEC-009` en curso para la base normativa v2.

## 2. Hardware objetivo

- Equipo: GEEKOM Mini IT13.
- CPU: Intel Core i9 de 13.ª generación.
- RAM: aproximadamente 32 GB.
- GPU: NVIDIA RTX 5060 Ti.
- VRAM: 16 GB GDDR6.
- Conexión: eGPU mediante USB4.
- Backend: CUDA 13.5.

## 3. Mapa operativo

- `src/`: scripts `.bat` de ejecución por modelo; se versionan. Actualmente solo conserva `.gitkeep`.
- `models/`: modelos descargados; contiene tres archivos `.gguf` bajo `models/gemma/` y no se versiona.
- `bin/`: dependencias y versiones precompiladas o compiladas de llama.cpp, excluidas de Git.
- `llama.cpp/`: repositorio oficial para consulta y compilación local; nunca se modifica.
- `docs/`: documento maestro, flujo Git y corpus SDD.
- `docs/constitution.md`: norma suprema de rango 1.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable de rango 3.
- `docs/sdd/plantillas/`: contratos de artefactos de rango 5, incluidas las plantillas de informe analítico y de auditoría.
- `docs/sdd/README.md`: índice del corpus y orden de precedencia.
- `docs/sdd/firmantes_autorizados`: claves públicas que habilitan las aprobaciones firmadas.
- `specs/`: registro `INDEX.md` y artefactos de cada spec en `NNN-slug/`.
- `tools/sdd/`: validador determinista (`validate.py`, `validate.bat` y `tests/`).
- `.opencode/`: cinco agentes (`sdd`, `planner`, `coder`, `reviewer`, `documenter`), comandos `sdd-*` y skills. El rol de auditoría está declarado en la base; su implementación corresponde a B3.
- `main.bat`: menú principal implementado para seleccionar scripts de `src/`.
- `CHANGELOG.md`, `README.md` y `MEMORY.md`: registro de cambios, descripción y contexto operativo.
- `logs/`, `results/` y `tmp/`: resultados temporales y archivos locales excluidos.

## 4. Enfoque SDD

- Modelo: **Spec-Anchored**. La especificación y el código conviven y se validan mutuamente.
- Ciclo de siete etapas: Specify, Clarify, Plan, Tasks, Implement, Validate y Release.
- Estados: `draft`, `clarified`, `planned`, `tasked`, `implementing`, `implemented`, `validated`, `released`, `cancelled` y `superseded`.
- Compuertas: G1 cierra Clarify, G2 cierra Tasks, G3 cierra Implement, G4 cierra Validate, G5 autoriza la integración y G6 autoriza el release.
- Aprobaciones humanas: G1 y G4 se registran en `spec.md`; G6 en la entrada del release de `CHANGELOG.md`. Solo valen dentro de un commit firmado por una clave de `docs/sdd/firmantes_autorizados`.
- Verificaciones: G2, G3 y G5 las verifica y registra el orquestador; no constituyen aprobación humana.
- Identificadores: `SPEC-001`, `RF-001`, `RNF-001`, `CB-001`, `AMB-001`, `CA-001`, `T-001`, `DEC-001`, con tres dígitos y sin reutilización.
- Trazabilidad obligatoria: `RF/CB → CA → T → evidencia`.
- Requisitos en notación EARS, con umbral numérico y unidad cuando corresponda.
- Versionado de specs: 0.1.0 inicial, MINOR por etapa de contrato, PATCH editorial, reapertura con motivo y versión, y prohibición de renumerar una spec publicada.
- Legado: `SPEC-001` a `SPEC-007` se conservan y su regularización corresponde a una spec posterior.
- Excepción sin spec: solo el cambio exclusivamente editorial, con commit `docs:` o `chore:`.

## 5. Regla crítica sobre `llama.cpp/`

Nunca crear, modificar, eliminar, mover, renombrar o sobrescribir archivos o carpetas dentro de `llama.cpp/`.

La carpeta `llama.cpp/` solo debe utilizarse para:

1. Consultar documentación y código de referencia.
2. Generar compilaciones para el hardware local específico.

Antes de compilar localmente, el repositorio oficial debe estar clonado en `llama.cpp/`. No generar nuevas salidas dentro de esa carpeta, incluida cualquier carpeta `build/`; los artefactos deben quedar fuera, preferiblemente en `bin/`.

Para ejecutar versiones precompiladas no es necesario clonar ni compilar `llama.cpp/`.

## 6. Reglas de ejecución

- Los `.bat` resuelven la raíz mediante `%~dp0`.
- No dependen del directorio actual ni del `PATH` del sistema.
- Seleccionar explícitamente el ejecutable y el archivo `.gguf`.
- Verificar que existan el ejecutable y el modelo antes de iniciar.
- No colocar modelos dentro de `bin/`.
- No colocar binarios dentro de `models/`.
- No eliminar ni modificar `.gitkeep` mientras las carpetas correspondientes deban permanecer inicializadas.

## 7. Parámetros iniciales

- GPU offload: `-ngl 99`.
- Carga del modelo: `-lm none`.
- Modelos de 20B o más: comenzar con `-np 1`.
- Modelos de 10B-15B: probar inicialmente con `-c 8192`.
- Modelos de 20B-24B: validar VRAM antes de usar contextos largos.
- Modelos de 25B-28B: comenzar con `-c 4096 -np 1`.
- Arquitecturas tipo Gemma: comenzar con `-fa off`.
- Modelos de 30B-35B: usar cuantización Q3, `-c 4096` y `-np 1`.

## 8. Criterios de validación

Antes de considerar funcional u optimizado un script, comprobar:

- Que el ejecutable exista.
- Que el modelo exista.
- Que la configuración corresponda al modelo.
- Consumo de VRAM y RAM.
- Tokens por segundo.
- Si existe desbordamiento hacia memoria compartida.
- Versión concreta de llama.cpp utilizada.

No asumir que el resultado de `llama-bench` representa el rendimiento de un servidor con contexto largo.

## 9. Git, MCP y secretos

- Ramas de trabajo `feat/*`, `fix/*` y `hotfix/*`; empaquetado en `release/vX-Y-Z`.
- Integración exclusiva por Pull Request con `merge --no-ff`; rebase, squash y copia manual están prohibidos.
- Tags anotados `vMAJOR.MINOR.PATCH` con mensaje `Release vX.Y.Z` y commit objetivo verificado.
- `main` y `dev` protegidas: sin commit ni push directos.
- La rama de trabajo se elimina tras confirmar la integración y `dev` se sincroniza con `main` antes del empaquetado.
- Antes de cada release menor se ejecuta una auditoría de conformidad y su informe se registra en la entrada del release.
- Servidores MCP con sufijo `-mcp`; las herramientas se referencian con el nombre completo del servidor.
- Sin tokens ni credenciales en archivos versionables; `example.env` es la plantilla y `.env` permanece protegido.

## 10. Referencias

- `docs/constitution.md`: norma suprema.
- `AGENTS.md`: reglas operativas de agentes.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable del proceso.
- `docs/sdd/README.md`: índice del corpus y precedencia.
- `docs/Flujo_de_Trabajo_Git.md`: procedimiento Git.
- `docs/Documento_Maestro_Consolidado_Arquitectura_de_IA_Local_y_Benchmarking_de_eGPU_16GB_VRAM.md`: arquitectura y benchmarks.
- `specs/INDEX.md`: registro de especificaciones.
