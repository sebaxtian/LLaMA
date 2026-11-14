# Constitución del proyecto LLaMA

Este documento es la **norma suprema** del repositorio. Su rango es **1** y su carácter es **normativo**: prevalece sobre `AGENTS.md`, sobre el protocolo operativo, sobre el flujo Git, sobre las plantillas, sobre las specs y sobre el código. Ante cualquier contradicción entre esta constitución y otro documento, prevalece esta constitución y el trabajo se detiene hasta corregir el documento de rango inferior.

## 1. Identidad y misión

- El proyecto `LLaMA` ejecuta, prueba y compara modelos LLM localmente mediante [llama.cpp](https://github.com/ggml-org/llama.cpp) en Windows 11, sin dependencia de servicios externos.
- Plataforma: Windows 11 sobre hardware GEEKOM Mini IT13, CPU Intel Core i9 de 13.ª generación, RAM aproximada de 32 GB y GPU NVIDIA RTX 5060 Ti con 16 GB de VRAM conectada por eGPU USB4.
- Caso de uso principal: programación en Python, análisis de datos y arquitectura de software.
- Misión: obtener ejecuciones locales reproducibles y medibles por modelo, con evidencia registrada de carga, consumo de memoria y velocidad.
- El desarrollo se rige estrictamente por **Desarrollo Basado en Especificaciones (SDD)** en su variante **Spec-Anchored**: la especificación y el código conviven y se validan mutuamente. No se adopta Spec-as-Source ni Spec-First.

## 2. Principios innegociables

1. **Especificación previa.** Ninguna feature, fix, refactor o cambio de configuración se implementa sin una spec aprobada. La única excepción es el cambio exclusivamente editorial, registrado con commit `docs:` o `chore:`.
2. **Determinismo.** Cada requisito, criterio, tarea y validación se redacta de modo que dos agentes independientes obtengan el mismo resultado sin interpretación adicional.
3. **Trazabilidad total.** Cada requisito se vincula a criterios de aceptación, tareas y evidencia conforme a la cadena `RF/CB → CA → T → evidencia`. Ningún requisito queda sin criterio, ningún criterio sin tarea y ninguna tarea sin evidencia.
4. **Aprobación humana por commit firmado.** La aprobación de una compuerta se registra como línea explícita y solo vale dentro de un commit firmado por una clave de la lista de firmantes autorizados. Si la firma falta, no verifica o la clave no figura en esa lista, la compuerta no está aprobada.
5. **Menor privilegio.** Cada agente recibe solo los permisos que su función exige y no escribe fuera de las rutas que tenga asignadas.
6. **Verificabilidad.** Ninguna afirmación de éxito se declara sin evidencia registrada en el reporte de validación de la spec.

## 3. Guardrails de archivos

- `llama.cpp/`: repositorio oficial de solo lectura. Prohibido crear, modificar, eliminar, mover, renombrar o sobrescribir cualquier archivo o carpeta de su interior; se usa para consultar documentación y código de referencia y para generar compilaciones cuyos artefactos quedan fuera de esa carpeta.
- `bin/`: dependencias y versiones precompiladas o compiladas de llama.cpp, excluidas de Git. Prohibido colocar modelos dentro.
- `models/`: modelos descargados, excluidos de Git. Prohibido colocar binarios dentro.
- `.env`: credenciales locales, excluido de Git y protegido contra lectura y edición. La plantilla versionable es `example.env`.
- `.gitkeep`: se conservan `bin/.gitkeep`, `models/.gitkeep` y `src/.gitkeep` para mantener inicializadas esas carpetas en clones limpios.

## 4. Stack

- Herramientas de proceso y validación: **Python** con biblioteca estándar, sin dependencias externas para el validador.
- Ejecución de modelos: scripts **`.bat`** para Windows, que resuelven la raíz con `%~dp0` y no dependen del directorio actual ni del `PATH`.
- Control de versiones: **Git**, con el procedimiento de `docs/Flujo_de_Trabajo_Git.md`.
- Plataforma: **Windows 11** con backend CUDA sobre GPU NVIDIA.

## 5. Estándares de calidad

- **TDD estricto** para código Python: prueba que falla, implementación mínima que la satisface y refactor con la suite en verde.
- **Validación-first** para scripts `.bat`: comando, salida esperada, código de salida y métricas se declaran antes de implementar.
- `AGENTS.md` se mantiene entre **30 y 70 líneas útiles**.
- Cada cambio relevante se registra en `CHANGELOG.md` bajo `Unreleased` hasta publicar el release.
- Idioma de la documentación: **español**, en Markdown y texto plano.
- Un script se declara validado solo si se ejecuta correctamente con el modelo configurado; el resultado de `llama-bench` no sustituye la validación de un servidor con contexto largo.

## 6. Jerarquía normativa

La autoridad se ordena en siete rangos; entre rangos distintos prevalece el de número menor.

| Rango | Documento | Carácter | Desempate dentro del rango |
|---|---|---|---|
| 1 | `docs/constitution.md` | Norma suprema | Documento único del rango |
| 2 | `AGENTS.md` | Norma operativa para agentes | Documento único del rango |
| 3 | `docs/sdd/PROTOCOLO_OPERATIVO.md` | Norma ejecutable del proceso | Documento único del rango |
| 4 | `docs/Flujo_de_Trabajo_Git.md` | Norma de integración y release | Documento único del rango |
| 5 | `docs/sdd/plantillas/*.md` | Norma de forma de cada artefacto | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md`, este sobre `validation_report.md`, este sobre `informe_analitico.md` y este sobre `informe_auditoria.md` |
| 6 | `specs/NNN-slug/*.md` | Contrato de la feature | `spec.md` prevalece sobre `clarify.md`, este sobre `plan.md`, este sobre `tasks.md` y este sobre `validation_report.md` |
| 7 | `src/`, `tools/`, `tests/`, `.opencode/` | Implementación verificable | El código no prevalece sobre norma alguna; su divergencia se corrige en el código |
| Sin rango | Guías de `docs/sdd/`, informes de análisis, informes de auditoría, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `CHANGELOG.md` | Referencia no normativa; el índice `docs/sdd/README.md` declara el desempate del rango y `CHANGELOG.md` registra G6 | Sin precedencia: no fija reglas |

Reglas de resolución:

- Dentro de un rango, el desempate lo fija el orden de precedencia que `docs/sdd/README.md` declara para ese rango.
- Una contradicción entre rangos, o dentro de un rango sin orden declarado, **detiene el trabajo** y se registra como defecto de la base.
- La corrección se aplica primero en el soporte de mayor rango y después en el de menor rango que quedó desalineado.
- La categoría sin rango no fija reglas: una contradicción con un documento normativo se resuelve a favor del documento normativo y la corrección se aplica en el documento sin rango.

El proceso declara seis compuertas —G1, G2, G3, G4, G5 y G6— y diez estados —`draft`, `clarified`, `planned`, `tasked`, `implementing`, `implemented`, `validated`, `released`, `cancelled` y `superseded`—; el protocolo operativo desarrolla la condición, la evidencia y la transición de cada uno. Los documentos de la base declaran el mismo conjunto de compuertas, estados y roles, y una divergencia se resuelve por rango.

## 7. Gobernanza y aprobaciones

- **Propietario:** `Agent Sebaxtian` (`agent@sebaxtian.dev`). Es el único declarante de las compuertas G1, G4 y G6.
- **Firmantes autorizados:** la lista se versiona en `docs/sdd/firmantes_autorizados`, contiene solo claves públicas en el formato de lista de firmantes admitidos de Git y la mantiene el propietario. Ninguna clave privada se incorpora al repositorio.
- **Registro de aprobaciones:** G1 y G4 se registran en la sección de aprobaciones de `spec.md`; G6 se registra en la entrada del release de `CHANGELOG.md`. Cada compuerta tiene una sola ubicación y el reporte de validación no porta casilla de aprobación.
- **Mecanismo de firma:** el propietario firma sus commits con una clave registrada en Git local y su clave pública figura en la lista de firmantes. La línea de aprobación solo vale dentro de un commit firmado por una clave de esa lista, y la verificación contrasta la firma de ese commit con la lista.
- **Sección protegida:** la sección de aprobaciones de `spec.md` y la entrada del release en `CHANGELOG.md` solo las modifica el propietario mediante un commit firmado. Ningún agente las escribe ni las rellena.
- **Prohibición de autoaprobación:** ningún agente aprueba su propia spec, su propia implementación ni su propio release, y ningún agente declara una compuerta. Un agente que redacta una línea de aprobación produce un registro sin valor y el caso se trata como incumplimiento.
- **Firma ausente o no verificada:** si la firma falta, no verifica o la clave no figura en la lista de firmantes, la compuerta no se considera aprobada y el caso se registra como incumplimiento.
- **Roles:** los seis roles de agente son orquestador, planner, documenter, coder, reviewer y auditor. El propietario es la persona que aprueba y no forma parte de la matriz de agentes. El rol de auditoría tiene lectura sobre la base normativa completa, sin permiso de modificar requisitos y sin permiso de aprobar compuertas; su implementación en `.opencode/` corresponde al bloque B3.

## 8. Control de cambios de la base

- Un cambio de esta base exige spec aprobada, incremento de la versión del documento y entrada en `CHANGELOG.md` bajo `Unreleased`.
- Se prohíbe integrar un cambio de la base sin spec aprobada. La única excepción es el cambio exclusivamente editorial, que no altera reglas ni requisitos.
- Antes de cada release menor se ejecuta una auditoría de conformidad sobre la base vigente, se conserva su informe y se registra su identificador en la entrada del release. Sin ese informe no se emite G6.
- La auditoría de conformidad la ejecuta el rol de auditoría y su informe sigue la plantilla de informe de auditoría de rango 5.
- Una corrección que altere el significado de una regla no es editorial: exige spec aprobada y revisión de conformidad.

## 9. Prohibiciones

- Integrar un cambio sin la compuerta que lo autoriza cumplida.
- Integrar por una vía distinta de `merge --no-ff`: rebase, squash merge o copia manual de cambios están prohibidos.
- Crear tags no anotados o con formato distinto de `vMAJOR.MINOR.PATCH`.
- Efectuar commit o push directo sobre `main` o `dev`: cada cambio entra por Pull Request.
- Incorporar al repositorio modelos, binarios, dependencias, credenciales, controladores, firmware o contenido de `llama.cpp/`.
- Modificar requisitos de una spec para ajustarlos al código implementado.
- Declarar un modelo «optimizado» sin comprobar carga, consumo de VRAM y RAM, desbordamiento a memoria compartida y velocidad.

## 10. Legado y transición

- **Cláusula de legado:** las specs publicadas `SPEC-001` a `SPEC-007` conservan su contenido y quedan amparadas por esta cláusula; su regularización corresponde a una spec posterior y no se ejecuta por edición directa.
- **Sustitución en la misma ruta:** cada documento de la base se sustituye en su ruta y con su nombre; no se crean copias paralelas ni documentos vigentes duplicados para una misma materia.
- **Historial:** las versiones anteriores de cada documento sustituido permanecen en el historial Git y no se copian a rutas de archivo.
- **Vigencia:** las specs posteriores a `SPEC-007` se rigen por esta base desde su publicación.
