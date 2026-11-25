# Changelog

Todos los cambios importantes del proyecto `LLaMA` se documentan en este archivo.

El formato sigue una estructura compatible con Semantic Versioning:

```text
vMAJOR.MINOR.PATCH
```

## [Unreleased]

### Added

- Catálogo de 9 escenarios de ejecución del modelo (`SPEC-018`): 1 escenario por combinación de 0, 6 y 9 capas de expertos en CPU con contexto de 4 096 tokens, 131 072 tokens y contexto ajustado, con identificadores canónicos `ESC-M0-C4K` a `ESC-M9-CADJ`, presupuesto de VRAM desglosado en 4 componentes con margen libre mínimo de 512 MiB y memoria de sistema requerida por escenario.
- Selector de escenario por argumento de línea de órdenes y por menú interactivo, con enumeración determinista, código de salida específico para identificador inexistente y verificación de recursos antes del lanzamiento.
- Registro de conformidad presupuestaria por escenario, con el exceso declarado en MiB y la medición conservada íntegra.
- Revocación de la aprobación de un escenario cuando cambia cualquiera de los 4 valores que la sostuvieron, con motivo que nombra el valor y exigencia de medición nueva.

### Changed

- Deuda del régimen registrada durante `SPEC-018`: la comprobación `C-17` exige la línea `Merge: <sha>` cuando la spec pasa a `validated`, y ese identificador solo existe después de integrar la rama que transporta la transición `T6`. La integración se hace por tanto en 2 pasos: primero con la spec en `implemented`, después con la transición y el identificador reales.
- Deuda del régimen registrada durante `SPEC-018`: el protocolo no declara transición desde `implemented` para una brecha de implementación descubierta en la etapa Validate; la reapertura practicable es `T11`, que exige cambio de requisito aprobado y anula la aprobación `G1`.

## [v0.8.0] - 2026-11-24

### Added

- Configuración ejecutable y medible de `Gemma-4-26B-A4B-it-qat-GGUF` con 3 perfiles versionados (`rendimiento`, `resiliencia`, `sin_especulativa`), presupuesto de VRAM medido en la máquina objetivo, registro de 22 campos con memoria de expertos en host y documentos de línea base con sus 3 secciones (`SPEC-017`).
- Sonda de contexto sostenido con `ignore_eos` y clasificación por `timings`, comparación de desviaciones con bloque de `C-7` y elegibilidad de promoción por huella, derrame y VRAM libre (`SPEC-017`).
- Transición `T11` del protocolo operativo y del validador: reversión a `draft` desde `tasked`, `implementing`, `implemented` o `validated` cuando el propietario aprueba un cambio de requisito.
- Informe final de auditoría `docs/sdd/auditoria_final_v0_8_0.md`, ejecutado sobre el árbol de la rama de cierre: cierre de los 5 hallazgos del informe previo —`H-02` por ratificación del propietario mediante el acta `docs/sdd/ratificacion_t11.md` firmada en `a06c789`, y `H-01`, `H-03`, `H-04` y `H-05` con el registro de cambios, el registro de G5, `MEMORY.md` y el historial de la spec—, con 0 hallazgos abiertos, 5 observaciones de severidad `Baja` y veredicto `CONFORME`; el inventario registra `AUD-114` a `AUD-118` y el índice del corpus las filas 42 a 44 (`SPEC-017`).

### Changed

- Contrato de `SPEC-017`: `RNF-003` mide derrame no intencional de como máximo 512 MiB —`Shared Usage` menos expertos en host— y `RNF-007` rige como condición de promoción sobre la última carga registrada; `RF-006` declara 22 campos y `C-2` nueve ejes con caché KV `q8_0` y `flash_attn on`.
- Perfiles `rendimiento` y `resiliencia` adoptan `ncmoe` 9 por comparación medida; la caché KV cuantizada reduce la caché no-SWA a 10,625 MiB por 1024 tokens y fija la SWA en 159,38 MiB.

### Fixed

- Documento `docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md` sin doble codificación ni marca de orden de bytes, con las 3 secciones de `C-10` y las marcas de estado de los perfiles.
- Lectura tolerante de los registros de 21 filas anteriores a la ampliación a 22 campos, con el campo 22 sintetizado en `no disponible` y sin reescribir el histórico.
- Approved by: Agent Sebaxtian

## [v0.7.2] - 2026-11-21

### Added

- Régimen de conformidad determinista de `SPEC-016`: inventario único en `docs/sdd/inventario_hallazgos.md` con 82 filas de los cinco informes anteriores, cada una con los ocho campos de `RF-011`, la cita de la regla con la forma `ruta §capítulo:línea` y el estado que declara el informe más reciente, más la sección §8 con las 3 filas de `AUD-111` a `AUD-113`; el veredicto se calcula desde el estado de las filas con la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME`, y la tabla de cierre acredita los 16 hallazgos del corte, 11 por artefacto y 5 por ratificación.
- Conjunto único de seis artefactos de empaquetado declarado con las claves `A1` a `A6` en §15 de `docs/sdd/PROTOCOLO_OPERATIVO.md` y en el paso 3 de `docs/Flujo_de_Trabajo_Git.md`, con su modificación admitida y la exigencia de spec previa o fix previo para cualquier otra ruta (`SPEC-016`, `AUD-103`).
- Fila de orden de lectura 36 en la tabla de inventario de `docs/sdd/README.md` para `docs/sdd/inventario_hallazgos.md`, con rango «Sin rango» y el cauce de escritura del `documenter` antes de integrar un informe de auditoría (`SPEC-016`).
- Informe final de auditoría `docs/sdd/auditoria_final_v0_7_2.md`, ejecutado sobre el commit `104496d` de `dev`: once dimensiones evaluadas, veredicto calculado desde las 85 filas del inventario, 0 hallazgos abiertos y 4 observaciones de severidad `Baja`, `OBS-005` a `OBS-008`; el ciclo de auditoría del release emite ocho observaciones de severidad `Baja` entre el informe previo y el final, y esta entrada transcribe el identificador del informe final y el recuento de 0 hallazgos abiertos (`SPEC-016`, `RF-015`).

### Changed

- §16 de `docs/sdd/PROTOCOLO_OPERATIVO.md` y la lista de prohibiciones de `docs/sdd/plantillas/spec.md` declaran que ninguna spec fija el veredicto, el recuento de hallazgos ni el conjunto de dimensiones de un informe posterior a su aprobación, y que la forma prohibida se registra como hallazgo que impide G1 (`SPEC-016`).
- Regularización de la comprobación del historial de releases: exige una fila por release publicado, admite las filas de historial de cambios y de transición que el empaquetado escribe y la constante de estados que admite `released` (`SPEC-016`, `AUD-088`).
- Ratificación firmada del propietario sobre las modificaciones del commit `564bac4` en artefactos publicados: 3 rutas afectadas (`CHANGELOG.md`, `specs/014-cierre-observaciones-finales/spec.md` y `specs/013-cierre-reauditoria-conformidad/validation_report.md`), junto con el caso `494db2e`; efecto declarativo: el contenido publicado se conserva y la autoría queda acreditada por el acta de `docs/sdd/ratificacion_historica.md`, firmada en `9042ae6` con estado `G`, que cierra por ratificación las 5 exenciones `AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053` (`SPEC-016`, `RF-004`, `RF-014`, `AUD-090`, `AUD-104`).
- Ratificación de interpretación del §16 del protocolo en `docs/sdd/ratificacion_interpretacion.md`, firmada en el commit `8c8a2a3`: la prohibición alcanza a declarar por anticipado el veredicto y a fijar por anticipado el recuento o el conjunto de dimensiones, y no alcanza a condicionar la publicación a la verificación de un estado del inventario; `AUD-111` queda en estado `cerrado por ratificación` (`SPEC-016`, `RF-014`).
- Reapertura de `SPEC-016` autorizada por el propietario por los hallazgos `H-01`, `H-02` y `H-03` del informe previo al release: la spec pasa de 0.8.0 a 0.9.0 y registra 0.9.1, 0.9.2 y 0.9.3 con la corrección de `RF-015` y `CA-016`, el alcance del inventario, el límite del permiso del `reviewer` y las observaciones `OBS-001` a `OBS-004`; el ciclo reabierto cierra 36 de 36 tareas y 39 de 39 filas en `PASADO`.

### Fixed

- Permiso del `reviewer` y autoría de las notas append-only: §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` atribuye la redacción de la nota del reporte de una spec publicada al `documenter` y su firma al propietario en un commit firmado con una clave de `docs/sdd/firmantes_autorizados`, limita al `reviewer` al reporte de la spec en curso y declara que su concesión no alcanza `specs/*/validation_report.md` sin límite de spec; el rol declara el mismo límite en `.opencode/agents/reviewer.md:104` y `:109` y `AUD-112` queda cerrado (`SPEC-016`, `RF-016`).
- Consistencia de `MEMORY.md` con el frontmatter de `spec.md` y con `specs/INDEX.md:22`: declara `SPEC-016` validada, con release pendiente y sin tag de release, cita el índice como fuente del estado y registra la corrección en la fila 0.9.1 del historial de cambios de la spec; `AUD-113` queda cerrado (`SPEC-016`, `RF-017`).
- Observaciones del informe previo al release: la fila `AUD-108` cita `specs/015-cierre-auditoria-posterior/spec.md:293`, `docs/Flujo_de_Trabajo_Git.md:235` declara las 222 pruebas del mecanismo, las fechas de las dos tablas de `SPEC-016` se declaran documentales en UTC y la fila T6 del primer ciclo retira la integración posterior a G4, que el ciclo reabierto reproduce y queda registrada como `OBS-007` (`SPEC-016`).

- Approved by: Agent Sebaxtian

## [v0.7.1] - 2026-11-21

### Added

- Procedimiento de corrección de un tag publicado en `docs/Flujo_de_Trabajo_Git.md`: exige de forma simultánea la autorización escrita del propietario, el registro del identificador del tag anterior y del destino nuevo, y la ausencia de consumidores que dependan del tag; desplaza la corrección a un release PATCH nuevo cuando existe consumidor y conserva la prohibición de mover, eliminar o reutilizar un tag publicado, con el caso `v0.7.0` registrado como deuda aceptada entre el tag anterior `ad739a0` y el destino vigente `5a3af48` (`SPEC-015`, `AUD-087`).
- Alcance cerrado de la rama `release/vX-Y-Z` en el paso 3 del procedimiento de release y en la excepción de ramas de release de `docs/Flujo_de_Trabajo_Git.md`: cuatro artefactos admitidos —`CHANGELOG.md`, `specs/INDEX.md`, el frontmatter de las specs publicadas y la línea `Release:` de los reportes publicados—, exigencia de spec previa o fix previo para cualquier otra ruta y detención del empaquetado con el registro del hallazgo; el empaquetado de `v0.7.0` queda registrado como excepción con el commit `5da6df6` y sus 18 archivos (`SPEC-015`, `AUD-088`).
- Firma obligatoria posterior a la publicación en `docs/Flujo_de_Trabajo_Git.md`: cada modificación de una entrada de release o de un artefacto de una spec publicada consta en un commit firmado por el propietario con una clave de `docs/sdd/firmantes_autorizados`, el estado de firma se transcribe en la evidencia del cierre y la firma del empaquetado no se extiende a las correcciones posteriores; el caso `494db2e` queda registrado con estado de firma `N` (`SPEC-015`, `AUD-090`).
- Nota append-only del resultado de G6 en el reporte de validación de `SPEC-014`, con las tres verificaciones de release y sin alteración de la matriz de 17 filas ni del dictamen `CONVERGIDO`, y nota de cierre corregida en el reporte de `SPEC-013`, que declara el valor efectivo `PARCIAL` de `RNF-001` y de `CA-015` y el cierre de las siete observaciones del informe final con seis cerradas con artefacto y `AUD-075` cerrada por `SPEC-015` (`SPEC-015`, `AUD-089`, `AUD-076`).
- Cierre de las diez observaciones de `docs/sdd/auditoria_posterior_v0_7_0.md` con el artefacto que satisface cada una y su evidencia transcrita por ruta y línea; `AUD-099` queda cerrada por la fila 34 de la tabla de inventario de `docs/sdd/README.md`, existente y sin modificación por `SPEC-015` (`SPEC-015`).

### Fixed

- La fila T7 del historial de transiciones de `SPEC-014` declara el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, en lugar del tag pendiente de la firma; la spec pasa a la versión 0.8.1 con una fila de motivo de regularización y conserva `status: released`, el campo `release: "v0.7.0"`, sus requisitos y sus criterios de aceptación (`SPEC-015`, `AUD-057`).
- §12 de `docs/sdd/PROTOCOLO_OPERATIVO.md` retira del bloque de documentos de raíz la remisión al bloque B3 y declara ejecutada la formalización de la allowlist de agentes, con referencia a la matriz de permisos vigente de los seis roles (`SPEC-015`, `AUD-068`).
- El párrafo posterior al historial de releases de `CHANGELOG.md` declara en tiempo pasado la línea de G6 registrada en la entrada del release y la creación del tag `v0.7.0`, y la viñeta de la entrada del release enumera los 16 identificadores asignados en lugar del rango que incluía números no asignados (`SPEC-015`, `AUD-100`).

### Registro del release

- G5: merge `4dd07f5` con dos padres; validación posterior a la integración sin hallazgos; rama `feat/cierre-auditoria-posterior` eliminada en local y en remoto.
- G6: resultado registrado en esta entrada con la línea de aprobación del propietario; las 3 verificaciones de release quedaron cumplidas sobre el estado publicado.
- Ancestría: `git merge-base --is-ancestor main dev` devuelve código 0 con `main` en `da30c86` y `dev` en `fbc6031`.
- Actualización documental: `specs/INDEX.md` y `CHANGELOG.md` actualizados con el release `v0.7.1` y con la línea de G6 firmada; la fila 21 de `specs/INDEX.md` declara el estado `released`.
- Tag anotado: el objeto del tag `v0.7.1` es un objeto de tipo `tag` con el identificador `4d0473b`, el mensaje `Release v0.7.1` y el commit objetivo `da30c86`, que coincide con `main`.

- Approved by: Agent Sebaxtian

## [v0.7.0] - 2026-11-14

### Added

- Cierre de las observaciones de los informes de auditoría de conformidad, con los identificadores `AUD-001` a `AUD-041` de la auditoría de origen y los identificadores `AUD-038`, `AUD-057`, `AUD-066`, `AUD-067`, `AUD-068`, `AUD-075`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-098`, `AUD-099`, `AUD-100`, `AUD-101` y `AUD-102` de la reauditoría final (`SPEC-013`, `SPEC-014`, `SPEC-015`).
- Informe de auditoría de cumplimiento SDD en `docs/sdd/auditoria_cumplimiento_sdd.md`: diez dimensiones evaluadas, 41 hallazgos con identificador `AUD-NNN`, hoja de ruta organizada en los bloques B1 a B4 y veredicto global `NO CONFORME` sobre el periodo de `SPEC-001` a `SPEC-007` (`SPEC-008`).
- Base normativa v2 (`SPEC-009`): mapa único de siete rangos, protocolo operativo redactado desde cero con sus dieciséis secciones, plantillas reconocidas como norma, contratos de informe analítico y de informe de auditoría, regla de versionado de specs, índice completo del corpus y lista `docs/sdd/firmantes_autorizados`. Fecha de corte `2026-11-14`.
- Rol `auditor` con lectura de la base completa y escritura limitada al informe que produce, implementado en `.opencode/agents/auditor.md` (`SPEC-011`).
- Integración continua en `.github/workflows/sdd.yml`: job `verify` que ejecuta la validación agregada y las dos suites de pruebas en cada Pull Request hacia `dev` y hacia `main`, con permiso de solo lectura y sin push, tag ni operación sobre el remoto (`SPEC-011`, `SPEC-014`).
- Comprobaciones nuevas del validador determinista: aprobación de G1, G4 y G6 contra `docs/sdd/firmantes_autorizados` y la firma del commit, cobertura de requisitos como error desde G2, detección de tareas abiertas en la ejecución agregada, G5 y G6 con lógica propia, transiciones e historial de transiciones, relación de sucesión y alcance exacto impreso en cada ejecución (`SPEC-010`).
- Trazabilidad profunda (`SPEC-012`): criterio de aceptación y evidencia obligatoria por tarea, sección de cierre de integración en el reporte de validación con el commit de integración y el tag del release, y regularización de `SPEC-001` a `SPEC-007` con esos campos.
- Informes `docs/sdd/auditoria_cierre_v0_7_0.md` y `docs/sdd/auditoria_final_v0_7_0.md`, con veredicto global `NO CONFORME` y `CONFORME CON OBSERVACIONES` respectivamente, y cierre registrado de las dieciséis observaciones de la reauditoría de cierre y de las cuatro observaciones que permanecían abiertas del informe final (`SPEC-013`, `SPEC-014`).

### Changed

- Registro único de aprobaciones: G1 y G4 en `spec.md` y G6 en este archivo; el reporte de validación no porta casilla de aprobación y la aprobación se acredita por commit firmado con una clave de `docs/sdd/firmantes_autorizados` (`SPEC-009`).
- Ciclo de siete etapas con máquina de estados, escritor y evidencia por transición, y compuertas con una sola condición de entrada, una sola evidencia, un solo declarante y una sola verificación (`SPEC-010`).
- Matriz de permisos de los seis roles con tres reglas de precedencia declaradas; el orquestador queda con escritura en `.opencode/**` como única concesión, sin contradicción con §12 del protocolo operativo (`SPEC-011`, `SPEC-014`).
- Flujo Git alineado con la base v2: compuertas G5 y G6, eliminación de la rama de trabajo tras la integración, check `verify` exigible con `strict: true` en `main` y en `dev`, verificación de ancestría entre `main` y `dev` en lugar del conteo de commits y gramática de ramas que admite `docs/` (`SPEC-009`, `SPEC-013`).
- Documentos de la base sustituidos en sus mismas rutas: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `docs/sdd/plantillas/`; las versiones anteriores permanecen en el historial Git y el detalle consta en el Anexo de transición del protocolo (`SPEC-009`).
- Se archiva la rama `feat/gemma-4-26b-a4b-it-qat-gguf` sin integrarla: dos commits no integrados, permanece local, no se publica y no se fusiona (`SPEC-009`).
- Guías, informes de análisis e informes de auditoría declaran su carácter de referencia no normativa; el índice `docs/sdd/README.md` cubre la raíz del corpus, las plantillas y los informes, y el inventario de documentos normativos se calcula desde ese índice (`SPEC-009`, `SPEC-013`).

### Fixed

- El mecanismo de control deja de repartir el registro de G4 entre dos artefactos y de evaluar G4 antes de existir el reporte que la propia compuerta exige; los estados `implementing`, `implemented` y `validated` quedan con escritor declarado (`SPEC-010`).
- La cobertura `RF/CB → CA` deja de producir solo advertencia y pasa a error desde G2, y G5 y G6 dejan de compartir la verificación de G4 (`SPEC-010`).
- El job `verify` deja de ejecutar una sola suite: prepara el árbol con historial completo y con las etiquetas del repositorio y ejecuta `tools/sdd/tests` y `tools/git/tests` (`SPEC-014`).
- Se cierran las observaciones de la reauditoría de cierre: flujo con `actions/checkout` y `actions/setup-python`, comprobación de sincronización de release expresada como ancestría verificable, gramática de ramas que admite `docs/`, dos ventanas de legado declaradas y atribución corregida de la escritura de transiciones (`SPEC-013`).
- Se registran como cerradas las cuatro observaciones finales, con nota de cierre append-only en el reporte de `SPEC-013` que transcribe el veredicto del informe final sin alterar la matriz ni el dictamen (`SPEC-014`).

- Approved by: Agent Sebaxtian

## [v0.6.0] - 2026-11-13

### Added

- Herramientas deterministas de aprovisionamiento y verificación de protección de ramas en tools/git/ (configure_branch_protection.py y verify_branch_protection.py) y especificaciones declarativas JSON (tools/git/protection_rules/).
- Suite de pruebas unitarias (test_verify_branch_protection.py) y pruebas de rechazo deterministas en repositorio remoto (test_remote_rejection.py) para verificación de ramas protegidas.

### Changed

- Configuración remota de GitHub para sebaxtian/LLaMA: protección clásica estricta en ramas main y dev (PR obligatorio, enforce_admins, sin force push ni borrado) y desactivación de fusiones squash y rebase en favor exclusivo de merge --no-ff.
- Actualización normativa de docs/Flujo_de_Trabajo_Git.md, docs/sdd/PROTOCOLO_OPERATIVO.md, AGENTS.md y MEMORY.md: formalización de ramas auxiliares de empaquetado release/vX-Y-Z, actualización de gramática de ramas y erradicación de commits directos en dev.

- Approved by: Agent Sebaxtian

## [v0.5.1] - 2026-11-13

### Changed

- La tabla de agentes del protocolo describe a `sdd` como orquestador de solo lectura sobre artefactos y código, con bookkeeping Git limitado a artefactos de control (`SPEC-006`).
- La memoria operativa enumera los agentes del proyecto y documenta cómo consultar la configuración cargada (`SPEC-006`).
- La clarificación de SPEC-005 registra la confirmación del propietario sobre la regla de celda superada (`SPEC-006`).

- Approved by: Agent Sebaxtian

## [v0.5.0] - 2026-11-13

### Added

- La compuerta G3 verifica que todas las tareas estén marcadas como completadas (`SPEC-005`).
- La compuerta G4 evalúa el estado real de la matriz de trazabilidad, incluidas las celdas compuestas (`SPEC-005`).

### Changed

- La comprobación de rama con Git se omite en las specs publicadas, cuya rama ya se integró (`SPEC-005`).
- SPEC-001 declara en sus criterios de aceptación la cobertura de los requisitos (`SPEC-005`).
- El protocolo describe el bookkeeping Git de `sdd` limitado a artefactos de control (`SPEC-005`).

- Approved by: Agent Sebaxtian

## [v0.4.0] - 2026-11-13

### Added

- Subagente `documenter` para correcciones editoriales y normativas en `docs/` y `AGENTS.md`, con permiso de edición acotado y sin terminal (`SPEC-004`).

### Changed

- G4 se describe como aprobación de la implementación validada en el protocolo operativo y en `AGENTS.md` (`SPEC-004`).
- El commit de release puede registrar `CHANGELOG.md`, `specs/INDEX.md` y el frontmatter de la spec del release (`SPEC-004`).
- Se documenta el criterio de incremento cuando un release combina correcciones con adiciones derivadas de ellas (`SPEC-004`).

- Approved by: Agent Sebaxtian

## [v0.3.1] - 2026-11-13

### Added

- Validación estricta de la compuerta G4 en `tools/sdd/validate.py`: dictamen por casilla marcada, filas no superadas y reporte obligatorio con G4, G5, G6 o estado validado (`SPEC-003`).
- Advertencia de cobertura `RF/CB → CA` mediante las líneas `Cubre:` de los criterios de aceptación (`SPEC-003`).

### Fixed

- La compuerta G4 ya no acepta «NO CONVERGIDO» como convergencia (`SPEC-003`).
- La detección de filas FALLADO o NO PASADO ahora evalúa las celdas reales de la matriz (`SPEC-003`).

- Approved by: Agent Sebaxtian

## [v0.3.0] - 2026-11-13

### Added

- Delegación del ciclo SDD desde el agente `sdd` hacia los subagentes `planner`, `coder`, `reviewer` y `explore` (`SPEC-002`).
- Sección de orquestación en `.opencode/agents/sdd.md` con tabla etapa-subagente, plantillas de solicitud y reglas de compuerta.

### Changed

- `planner` y `coder` usan `mode: all` para ejecutarse como agentes primarios y como subagentes (`SPEC-002`).
- `sdd` aplica una lista blanca de subagentes: `planner`, `coder`, `reviewer` y `explore`; el resto queda denegado (`SPEC-002`).
- `sdd` acota los comandos de shell con una regla general `ask` y una lista blanca: validador determinista, git de lectura, `git add` y `git commit` (`SPEC-002`).
- `planner` y `coder` deniegan el lanzamiento de subagentes (`SPEC-002`).

### Fixed

- La tabla de compuertas de `.opencode/agents/sdd.md` se alinea con `docs/sdd/PROTOCOLO_OPERATIVO.md` §2: Implement se verifica con G2 y G4 queda al final de Validate (`SPEC-002`).
- Se añaden los criterios de aceptación CA-007 a CA-010 y se alinea CB-001 a G2 (`SPEC-002`).

- Approved by: Agent Sebaxtian

## [v0.2.0] - 2026-11-12

### Added

- Configuración del proveedor local `LLaMA` en `opencode.jsonc` mediante la API compatible con OpenAI de llama.cpp.
- Metodología de Desarrollo Basado en Especificaciones (SDD) Spec-Anchored para el proyecto.
- `docs/constitution.md` como norma suprema del proyecto.
- `docs/sdd/PROTOCOLO_OPERATIVO.md` como norma SDD ejecutable (7 etapas, compuertas G1–G6, gramática de IDs, EARS).
- Corpus de referencia SDD versionado en `docs/sdd/` con índice en `docs/sdd/README.md`.
- Plantillas de artefactos SDD en `docs/sdd/plantillas/` (spec, clarify, plan, tasks, validation_report).
- `specs/INDEX.md` como registro canónico de especificaciones.
- Validador determinista `tools/sdd/validate.py`, envoltorio `validate.bat` y pruebas `unittest`.
- Agentes OpenCode `sdd`, `planner`, `coder` y `reviewer` en `.opencode/agents/`.
- Comandos `/sdd-spec`, `/sdd-clarify`, `/sdd-plan`, `/sdd-tasks`, `/sdd-implement`, `/sdd-validate`, `/sdd-status` y `/sdd-check`.
- Skills `sdd-lifecycle`, `ears-spec`, `sdd-plan-tasks`, `tdd-implement` y `llama-validation`.
- Normalización del corpus `docs/sdd/` (sufijo `-mcp`, IDs de 3 dígitos, rutas `specs/NNN-slug/`, `validation_report.md`).

- `main.bat` como menú raíz que descubre y ejecuta los scripts de `src/` (piloto `SPEC-001`).

### Changed

- Se actualizó `default_agent` a `plan` en `opencode.jsonc`.
- Se reescribió `AGENTS.md` para condensarlo en 30–70 líneas y alinearlo con la jerarquía normativa.
- Se añadieron permisos en `opencode.jsonc`: deny de edición en `bin/` y `models/`, y `ask` para `git push` y `git tag`.
- Se integraron las compuertas SDD (G5/G6) y las excepciones de bootstrap y editorial en `docs/Flujo_de_Trabajo_Git.md`.
- Se actualizaron `README.md` y `MEMORY.md` con la metodología SDD y la nueva estructura.

- Approved by: Agent Sebaxtian

## [v0.1.0] - 2026-11-10

### Added

- Servidor MCP remoto oficial de GitHub con toolsets limitados para contexto, repositorios, issues y pull requests.
- `example.env` como plantilla para `GITHUB_PERSONAL_ACCESS_TOKEN` sin credenciales reales.
- `opencode.jsonc` con configuración de proyecto, contexto operativo y protección de `llama.cpp/`.
- Estructura inicial del proyecto para ejecutar modelos LLM localmente con llama.cpp.
- Documentación de la arquitectura local y los benchmarks iniciales.
- `AGENTS.md` con las reglas operativas para agentes.
- `MEMORY.md` con la memoria operativa del proyecto.
- `README.md` con la guía general, arquitectura y flujo de trabajo.
- `LICENSE` con licencia MIT para el material propio del proyecto.
- `.gitignore` para excluir modelos, binarios, dependencias y el repositorio externo `llama.cpp`.
- Archivos `.gitkeep` para conservar inicializadas las carpetas `bin/`, `models/` y `src/`.
- Documento `docs/Flujo_de_Trabajo_Git.md` con la estrategia de ramas, releases y tags.

### Changed

- Se definió el flujo de trabajo basado en las ramas `main`, `dev`, `feat/*`, `fix/*` y `hotfix/*`.
- Se configuró la conservación explícita de `models/.gitkeep` en `.gitignore`.
- Se formalizó la estrategia de integración mediante `merge --no-ff`, sin rebase ni squash.
- Se definieron el bootstrap determinista de `main` y `dev`, la gramática de ramas y la política exacta de tags anotados.
- Se añadieron exclusiones para logs, resultados y archivos temporales locales.
- Se añadió la convención de nombres MCP con el sufijo `-mcp` y la exclusión de configuración local de `.vscode/`.
- Se actualizó la documentación operativa para distinguir la línea base normativa del flujo Git frente al estado histórico del repositorio.
- Se documentaron en `AGENTS.md`, `README.md` y `MEMORY.md` la configuración de `github-mcp`, el uso de `example.env` y la protección de credenciales locales.
- Se formalizó el procedimiento obligatorio de hotfix, resolución de conflictos, validación de tags y publicación de releases.
- Se definieron la gramática exacta de tags, el formato UTC del changelog y la regla para una sección `Unreleased` vacía.
- Se formalizaron la protección de `main` y `dev`, las validaciones por tipo de cambio y el registro obligatorio de autorización de releases.
- Se autorizó explícitamente el commit de preparación de release en `dev` como excepción exclusiva para actualizar `CHANGELOG.md`.
- Se actualizó el documento maestro con los benchmarks de Phi-4, Codestral 22B, Gemma-2-27B y Qwen2.5-Coder-32B, las matrices LM Studio/llama.cpp, el catálogo de modelos, los estados de validación y las configuraciones propuestas para la RTX 5060 Ti de 16 GB sobre USB4.
- Se sincronizó la documentación del estado Git actual y se creó `feat/sync-git-state` desde `dev`; la rama fue validada e integrada en `dev` mediante `merge --no-ff`.

### Fixed

- Se corrigió la exclusión accidental de `models/.gitkeep` para permitir que la carpeta `models/` permanezca inicializada en los clones.

### Removed

### Security

- Se excluye `/.env` de Git y se deniega a OpenCode su lectura y edición.

- Approved by: Agent Sebaxtian

## Historial de releases

Se publicó `v0.1.0` como primera versión estructural y documental del proyecto. El historial de releases con su fecha UTC y su tag anotado es:

| Versión  | Fecha      | Tag      |
| -------- | ---------- | -------- |
| `v0.1.0` | 2026-11-10 | `v0.1.0` |
| `v0.2.0` | 2026-11-12 | `v0.2.0` |
| `v0.3.0` | 2026-11-13 | `v0.3.0` |
| `v0.3.1` | 2026-11-13 | `v0.3.1` |
| `v0.4.0` | 2026-11-13 | `v0.4.0` |
| `v0.5.0` | 2026-11-13 | `v0.5.0` |
| `v0.5.1` | 2026-11-13 | `v0.5.1` |
| `v0.6.0` | 2026-11-13 | `v0.6.0` |
| `v0.7.0` | 2026-11-14 | `v0.7.0` |
| `v0.7.1` | 2026-11-21 | `v0.7.1` |
| `v0.7.2` | 2026-11-21 | `v0.7.2` |
| `v0.8.0` | 2026-11-24 | `v0.8.0` |

El empaquetado de `v0.7.0` quedó registrado en su entrada y en la tabla anterior: el release quedó publicado con la línea `- Approved by: Agent Sebaxtian` firmada por el propietario en el commit de empaquetado, G6 quedó cumplida y el tag anotado `v0.7.0` se creó sobre el commit publicado `5a3af48` con el mensaje `Release v0.7.0`.
