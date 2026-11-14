# Instrucciones operativas del proyecto LLaMA

Este documento es la **norma operativa** de rango **2**: cede ante `docs/constitution.md` (rango 1) y prevalece sobre `docs/sdd/PROTOCOLO_OPERATIVO.md` (rango 3) en materia operativa.
Ante contradicción con la constitución, prevalece la constitución y el trabajo se detiene; ante contradicción con el protocolo, prevalece este documento y la regla se corrige en el protocolo.

## Misión y stack

Repositorio para ejecutar, probar y comparar modelos LLM locales con llama.cpp en Windows 11, sin servicios externos.
Caso de uso principal: programación en Python, análisis de datos y arquitectura de software.
Hardware objetivo: GEEKOM Mini IT13, CPU Intel Core i9 de 13.ª generación, RAM de 32 GB y GPU NVIDIA RTX 5060 Ti de 16 GB de VRAM por eGPU USB4.
Ejecución: scripts `.bat` que resuelven la raíz con `%~dp0` y no dependen del directorio actual ni del `PATH`.
Herramientas de proceso: Python con biblioteca estándar, Git y Windows 11 con backend CUDA.

## Comandos

- `python tools\sdd\validate.py --all`: valida el corpus de specs.
- `python tools\sdd\validate.py --spec SPEC-NNN --gate G2`: valida una spec contra una compuerta.
- `python tools\sdd\validate.py --spec SPEC-NNN --gate G4 --git`: añade las comprobaciones Git.
- `python tools\sdd\validate.py --next-id`: devuelve el siguiente identificador libre.
- `opencode debug agents`: lista los agentes cargados desde la raíz del repositorio.

## Mapa del repositorio

- `docs/constitution.md`: norma suprema de rango 1.
- `AGENTS.md`: norma operativa de rango 2 para agentes.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable del proceso, rango 3.
- `docs/Flujo_de_Trabajo_Git.md`: norma de integración y release, rango 4.
- `docs/sdd/plantillas/`: norma de forma de cada artefacto, rango 5.
- `specs/NNN-slug/`: contrato de cada feature con sus artefactos.
- `src/`, `tools/`, `tests/` y `.opencode/`: implementación verificable de rango 7.
- `models/`: modelos descargados, excluidos de Git y sin binarios dentro.
- `bin/`: dependencias y versiones de llama.cpp, excluidas de Git y sin modelos dentro.
- `llama.cpp/`: repositorio oficial de solo lectura y referencia de compilación.
- `MEMORY.md`, `CHANGELOG.md` y `README.md`: contexto operativo, registro de cambios y descripción.

## Entrada SDD

Ninguna feature, fix, refactor o cambio de configuración se ejecuta sin spec aprobada en `specs/NNN-slug/`.
Ciclo de siete etapas: Specify, Clarify, Plan, Tasks, Implement, Validate y Release; el protocolo fija entrada, salida y responsable de cada una.
Estados admitidos: `draft`, `clarified`, `planned`, `tasked`, `implementing`, `implemented`, `validated`, `released`, `cancelled` y `superseded`.
Compuertas: G1 al cerrar Clarify, G2 al cerrar Tasks, G3 al cerrar Implement, G4 al cerrar Validate, G5 la integración y G6 el release.
Cada requisito se redacta en notación EARS y mantiene la cadena `RF/CB → CA → T → evidencia`.
Un cambio de requisito posterior a Clarify devuelve la spec a `draft` y exige nueva clarificación.
La numeración de identificadores usa tres dígitos y un identificador no se reutiliza.
Rol `auditor` (auditoría): lectura de la base completa, sin edición de requisitos y sin aprobación de compuertas; su implementación en `.opencode/` corresponde al bloque B3.

## Aprobaciones

G1 y G4 se registran solo en la sección de aprobaciones de `spec.md`; G6 se registra solo en la entrada del release de `CHANGELOG.md`.
Línea de registro: `- Approved by: Agent Sebaxtian`, válida solo dentro de un commit firmado por una clave de `docs/sdd/firmantes_autorizados`.
Ningún agente declara una compuerta ni escribe la sección protegida; la aprobación corresponde al propietario.
Un agente que redacta una línea de aprobación produce un registro sin valor y el caso se trata como incumplimiento.

## Guardrails

- `llama.cpp/`: solo lectura; prohibido crear, modificar, eliminar, mover, renombrar o sobrescribir contenido de su interior.
- `bin/` sin modelos dentro y `models/` sin binarios dentro; ambos excluidos de Git.
- `.env` protegido contra lectura y edición; `example.env` es la plantilla versionable.
- Se conservan `bin/.gitkeep`, `models/.gitkeep` y `src/.gitkeep`.
- Prohibido incorporar al repositorio modelos, binarios, dependencias, credenciales, controladores, firmware o contenido de `llama.cpp/`.
- Prohibido modificar requisitos de una spec para ajustarlos al código implementado.
- Prohibido declarar un modelo optimizado sin medir carga, VRAM, RAM, desbordamiento a memoria compartida y velocidad.

## Git

- Ramas de trabajo `feat/*`, `fix/*` y `hotfix/*`; ramas de empaquetado `release/vX-Y-Z` en minúsculas, números y guiones.
- Integración exclusiva por Pull Request con `merge --no-ff`; rebase, squash y copia manual están prohibidos.
- Tags anotados `vMAJOR.MINOR.PATCH` con mensaje `Release vX.Y.Z` y commit objetivo verificado.
- `main` y `dev` protegidas: sin commit ni push directos.
- La rama de trabajo se elimina tras confirmar la integración y `dev` se sincroniza con `main` antes del empaquetado.

## Validación

Antes de integrar: `git diff --check`, `git status --short`, revisión del alcance declarado y `python tools\sdd\validate.py --all`.
Un script se declara validado solo si se ejecuta con el modelo configurado; `llama-bench` no sustituye la prueba de un servidor con contexto largo.
El validador comprueba estructura, estados, trazabilidad y alcance declarado; no acredita la firma del commit de aprobación ni la conformidad del régimen.
Un resultado favorable del validador no autoriza compuerta alguna.

## MCP y secretos

- Servidores MCP con sufijo `-mcp`; las herramientas se referencian como `github-mcp_*`.
- Sin tokens ni credenciales en archivos versionables; `example.env` es la plantilla.

## Referencias

- `docs/constitution.md`: norma suprema de rango 1.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: norma ejecutable del proceso, rango 3.
- `docs/sdd/README.md`: índice del corpus y orden de precedencia; `docs/Flujo_de_Trabajo_Git.md`: procedimiento Git de rango 4.
