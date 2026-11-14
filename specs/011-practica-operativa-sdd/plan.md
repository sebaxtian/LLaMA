# Plan técnico — SPEC-011

*Artefacto de rango 6: diseño de la práctica operativa verificable de `SPEC-011`, con las decisiones `DEC-NNN` y la matriz de cobertura de la spec.*

## Referencias

- `spec.md`: `SPEC-011`, versión 0.2.0, estado `clarified`, con trece requisitos funcionales, ocho no funcionales, diecisiete casos borde y diecisiete criterios de aceptación.
- `clarify.md`: `SPEC-011`, cerrado con `AMB-001` a `AMB-008` resueltos, tres casos borde nuevos y once parches marcados.
- `docs/constitution.md`: principio de menor privilegio, guardrails de archivos y gobernanza de aprobaciones.
- `AGENTS.md`: matriz de roles y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §7 trazabilidad, §11 aprobaciones, §12 roles y permisos, §13 integración Git y §14 contrato del validador.
- `docs/sdd/plantillas/plan.md`: norma de forma de este artefacto.
- `docs/sdd/auditoria_cumplimiento_sdd.md`: hallazgos `AUD-061`, `AUD-063`, `AUD-064`, `AUD-071` y `AUD-081` a `AUD-084` y `AUD-091`.
- Estado observado del repositorio: seis archivos de rol en `.opencode/agents/` (cinco vigentes), `opencode.jsonc` con siete entradas de permiso, `.github/` sin flujo de integración, `AGENTS.md` con 67 líneas útiles y `tools/sdd/tests/test_validate.py` con 94 pruebas.

## Naturaleza del entregable

La spec produce configuración y documentación operativa verificable, sin código de ejecución de modelos:

- Seis archivos de rol en `.opencode/agents/` con matriz de permisos, allowlist de shell y política de subagentes; uno de ellos es el rol nuevo `auditor`.
- La configuración global `opencode.jsonc` con la precedencia declarada y las protecciones de `.env`, `llama.cpp/`, `bin/` y `models/`.
- El flujo de integración continua `.github/workflows/sdd.yml`.
- Un módulo de pruebas de configuración en `tools/sdd/tests/test_agent_permissions.py`.
- Dos actualizaciones de documentación operativa: `AGENTS.md` y `MEMORY.md`.
- La sección de cierre de práctica de `validation_report.md` con cinco filas de hallazgo, además de la matriz de trazabilidad con una fila por requisito y por caso borde.

No produce scripts `.bat`, no modifica la base normativa ni el validador, y no altera `src/`.

## Arquitectura

### Capas y responsabilidades

| Capa | Artefactos | Responsabilidad | Límite |
|---|---|---|---|
| Declaración de permisos | `.opencode/agents/*.md`, `opencode.jsonc` | Fija la matriz por rol, la allowlist de shell y la precedencia | No ejecuta verificación alguna |
| Verificación automatizada | `.github/workflows/sdd.yml` | Ejecuta el validador y la suite en cada Pull Request | No escribe en el repositorio ni opera sobre el remoto |
| Contraste de configuración | `tools/sdd/tests/test_agent_permissions.py` | Lee la declaración y resuelve el permiso efectivo | Solo lectura; no modifica archivos |
| Contexto operativo | `AGENTS.md`, `MEMORY.md` | Declara los seis roles y el estado del repositorio | No fija reglas nuevas |
| Evidencia | `validation_report.md` | Registra el cierre de los cinco hallazgos con su comando y su salida | Se completa en la etapa Validate |

### Resolución del permiso efectivo

El permiso efectivo se calcula con un procedimiento único, independiente del orden de la lista declarada:

1. Se reúnen las entradas cuyo `action` coincide con la operación y cuyo `resource` coincide con la ruta solicitada.
2. Si el conjunto está vacío, el permiso efectivo es `deny`; la ruta no declarada está denegada.
3. Del conjunto se conservan las entradas con la mayor especificidad. La especificidad cuenta los segmentos literales de la ruta; un segmento literal vale más que un comodín y el comodín recursivo vale menos que un comodín de un segmento.
4. En caso de empate de especificidad, `deny` prevalece sobre `allow` y sobre `ask`.
5. Una concesión de escritura no habilita la escritura de una línea de aprobación: la sección de aprobaciones de `spec.md` y la entrada del release de `CHANGELOG.md` no admiten concesión de rol alguno.

El resultado `ask` se reserva a las operaciones remotas del propietario y no se usa en la allowlist de ningún rol.

### Flujo de la verificación

| Paso | Origen | Acción | Destino |
|---|---|---|---|
| 1 | Pull Request a `dev` o `main` | Dispara el flujo | Trabajo `verify` en `windows-latest` |
| 2 | Trabajo `verify` | Instala Python 3.12 y ejecuta el validador agregado | Resultado del validador |
| 3 | Resultado en cero | Ejecuta la suite de pruebas | Resultado de la suite |
| 4 | Cualquier resultado distinto de cero | Finaliza en fallo e informa el paso | Pull Request bloqueado |
| 5 | Ambos resultados en cero | Finaliza en éxito sin operación remota | Pull Request habilitado para revisión |

## Contratos

### Contrato del archivo de rol

Cada archivo de `.opencode/agents/` declara un frontmatter con tres claves obligatorias y una lista de permisos:

| Clave | Forma | Regla |
|---|---|---|
| `description` | texto de una línea | Describe la función del rol |
| `mode` | `primary`, `subagent` o `all` | `reviewer`, `documenter` y `auditor` usan `subagent`; `planner` y `coder` usan `all`; `sdd` usa `primary` |
| `permissions` | lista de entradas | Primera entrada `action: edit`, `resource: "*"`, `effect: deny` |

Cada entrada de `permissions` ocupa tres líneas consecutivas con la forma `- action: <valor>`, `resource: <valor>` y `effect: <valor>`, con dos espacios de sangría. Los valores admitidos son `edit`, `read`, `shell` y `subagent` para `action`; `allow`, `deny` y `ask` para `effect`; y un patrón de ruta o de comando para `resource`. El cuerpo del archivo declara en una sección de permisos las cuatro reglas de precedencia y la allowlist de shell del rol.

### Contrato de la matriz de permisos

La lectura se declara como `allow` sobre `**` con `deny` explícito de `.env`. La escritura, el shell y los subagentes parten de `deny` sobre `*`.

| Rol | Modo | Escritura concedida | Denegaciones explícitas de escritura | Shell permitido | Subagentes |
|---|---|---|---|---|---|
| `sdd` | `primary` | `.opencode/**`, `.github/**`, `opencode.jsonc`, `MEMORY.md`, `specs/INDEX.md`, `specs/*/spec.md`, `specs/*/validation_report.md` | `src/**`, `tests/**`, `tools/**`, `docs/**`, `AGENTS.md`, `CHANGELOG.md`, `llama.cpp/**`, `bin/**`, `models/**`, `.env` | git de lectura, `git add`, `git commit`, validador | `planner`, `coder`, `reviewer`, `documenter`, `auditor`, `explore` |
| `planner` | `all` | `specs/**` | `specs/*/validation_report.md`, `src/**`, `tests/**`, `tools/**`, `docs/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `.opencode/**`, `.github/**`, `.env` | git de lectura, validador | denegados |
| `coder` | `all` | `src/**`, `tests/**`, `tools/**`, `specs/*/tasks.md` | `specs/**`, `docs/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `.opencode/**`, `.github/**`, `.env` | validador, suite de pruebas, git de lectura | denegados |
| `reviewer` | `subagent` | `specs/*/validation_report.md` | `specs/**`, `src/**`, `tests/**`, `tools/**`, `docs/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `.opencode/**`, `.github/**`, `.env` | git de lectura, validador | denegados |
| `documenter` | `subagent` | `docs/**`, `AGENTS.md` | `specs/**`, `src/**`, `tests/**`, `tools/**`, `.opencode/**`, `.github/**`, `opencode.jsonc`, `MEMORY.md`, `CHANGELOG.md`, `.env` | denegado | denegados |
| `auditor` | `subagent` | `docs/sdd/auditoria_*.md` | `docs/**`, `specs/**`, `src/**`, `tests/**`, `tools/**`, `.opencode/**`, `.github/**`, `AGENTS.md`, `MEMORY.md`, `opencode.jsonc`, `CHANGELOG.md`, `.env` | git de lectura, validador | denegados |

`.env` se deniega en lectura y en escritura para los seis roles. La allowlist de shell de cada rol se declara de forma literal y el comodín `*` de shell queda siempre en `deny`.

### Contrato de `opencode.jsonc`

El archivo conserva su forma JSONC y su bloque `permissions` declara cuatro protecciones y dos autorizaciones de propietario:

| Entrada | Acción | Recurso | Efecto |
|---|---|---|---|
| 1 | `edit` | `llama.cpp/*` | `deny` |
| 2 | `edit` | `bin/*` | `deny` |
| 3 | `edit` | `models/*` | `deny` |
| 4 | `read` | `.env` | `deny` |
| 5 | `edit` | `.env` | `deny` |
| 6 | `shell` | `git push *` | `ask` |
| 7 | `shell` | `git tag *` | `ask` |

Sobre el bloque se escribe un comentario con las cuatro reglas de precedencia y con el orden canónico de la lista. El archivo no incorpora credenciales ni secretos literales: el encabezado del servidor MCP conserva la referencia al entorno y no el valor de la credencial.

### Contrato del flujo de integración continua

| Campo | Valor | Motivo |
|---|---|---|
| Nombre | `SDD` | Identifica el flujo |
| Disparador | `pull_request` sobre `dev` y `main` | Cubre la integración y el empaquetado |
| Permisos del token | `contents: read` | Lectura mínima del repositorio |
| Ejecutor | `windows-latest` | Plataforma objetivo del proyecto |
| Python | 3.12 | Versión declarada por el propietario |
| Paso 1 | validador agregado del corpus | Verifica estructura, trazabilidad y compuertas |
| Paso 2 | suite de pruebas del mecanismo | Verifica el validador y la configuración |
| Límite del trabajo | 5 minutos | Umbral de 300 segundos de `RNF-001` |
| Límite del paso 2 | 1 minuto | Umbral de 60 segundos de `RNF-008` |
| Prohibiciones | push, tag, `secrets`, `deploy`, `continue-on-error` | `RF-007`, `RNF-002` y `CB-007` |

Cada paso se declara por separado y sin continuación en error, de modo que el fallo del primero no oculte el resultado del segundo; la salida de cada paso queda registrada en el registro del flujo.

### Contrato del módulo de pruebas de configuración

`tools/sdd/tests/test_agent_permissions.py` usa solo la biblioteca estándar y resuelve la raíz del repositorio con la ruta del propio archivo, sin importar el módulo del validador. Declara tres funciones auxiliares y diecisiete pruebas:

| Función | Entrada | Salida |
|---|---|---|
| `leer_permisos` | ruta del archivo de rol | lista de entradas con acción, recurso y efecto |
| `especificidad` | patrón de recurso | entero de segmentos literales |
| `resolver` | lista de entradas, acción y ruta | `allow` o `deny` según el procedimiento de la arquitectura |

| Prueba | Verifica |
|---|---|
| `test_seis_roles_declarados` | existen seis archivos con frontmatter y campos obligatorios |
| `test_contrato_de_entrada_de_permiso` | cada entrada declara acción, recurso y efecto admitidos |
| `test_denegacion_por_defecto` | la primera entrada de cada rol deniega la escritura y una ruta ajena a la declaración no se concede |
| `test_especificidad_prevalece` | el cierre de tareas del `coder` y el informe del `auditor` se conceden sobre una denegación general |
| `test_denegacion_prevalece_en_igual_especificidad` | un solapamiento sintético de igual especificidad se resuelve en denegación |
| `test_cero_conflictos_de_igual_especificidad` | las seis matrices no declaran una ruta a la vez con concesión y denegación de igual especificidad |
| `test_escritura_del_coder` | `src/`, `tests/`, `tools/` y el cierre de tareas se conceden; el resto se deniega |
| `test_escritura_unica_del_reviewer` | solo el reporte de validación se concede; el subagente y el shell de escritura se deniegan |
| `test_auditor_solo_informes` | el informe bajo `docs/sdd/auditoria_*.md` se concede y las rutas restantes de `docs/sdd/` se deniegan |
| `test_auditor_no_aprueba` | el rol carece de escritura sobre `spec.md`, `CHANGELOG.md` y las aprobaciones, y declara la regla en su cuerpo |
| `test_allowlist_de_shell` | cada rol deniega el shell general y su allowlist coincide con la declarada |
| `test_subagentes_por_rol` | solo el orquestador enumera subagentes; los cinco roles restantes deniegan el comodín |
| `test_configuracion_global` | `opencode.jsonc` declara las siete entradas, no contiene secreto literal y conserva la referencia al entorno |
| `test_estructura_del_flujo` | disparadores, ejecutor, versión de Python, dos pasos, límites y permisos del token coinciden con el contrato |
| `test_flujo_sin_efectos_remotos` | no hay disparador de push, ni `secrets`, ni `git push`, ni `git tag`, ni `deploy` |
| `test_documentacion_operativa` | `AGENTS.md` mantiene la longitud y menciona el rol; `MEMORY.md` menciona seis roles y la integración continua |
| `test_prueba_no_destructiva` | los archivos leídos conservan su huella y la ejecución completa en 60 segundos o menos |

Cada prueba de resolución construye sus escenarios en memoria y no escribe archivos: el módulo abre los artefactos en modo lectura y no ejecuta el cliente de agentes.

### Contrato del registro de evidencia

`validation_report.md` añade una sección de cierre de práctica con una fila por hallazgo y cuatro columnas: hallazgo, hecho acreditado, comando literal y resultado. El cierre de cada fila exige el hecho verificado y el código de salida cero; la fila que no acredite su hecho se escribe como abierta con el motivo consignado.

| Hallazgo | Hecho acreditado | Comando de verificación |
|---|---|---|
| `AUD-081` | la rama de integración contiene el commit publicado en `main` | `git rev-list --left-right --count dev...main` con salida `0 0` |
| `AUD-082` | la referencia remota del release anterior no existe | `git branch --all --list "*release/v0-6-0*"` sin resultados |
| `AUD-083` | la rama Gemma permanece local, no publicada y con decisión registrada | `git branch --list feat/gemma-4-26b-a4b-it-qat-gguf` con resultado y `git rev-parse --verify refs/remotes/origin/feat/gemma-4-26b-a4b-it-qat-gguf` sin resultado |
| `AUD-084` | los seis documentos están versionados y sin cambio pendiente | `git status --short --untracked-files=all -- docs/sdd/` sin entradas |
| `AUD-091` | `MEMORY.md` no contiene hechos obsoletos | `Select-String -Path MEMORY.md -Pattern "pendiente"` sin coincidencias y contraste de cada hecho declarado |

## Decisiones técnicas

### DEC-001

- **Decisión:** la precedencia se resuelve con el procedimiento de cinco pasos que fija la arquitectura, aplicado sobre el conjunto de entradas que coincide con la operación y la ruta, con independencia del orden de la lista. La denegación prevalece en igual especificidad y la ruta más específica prevalece sobre la general.
- **Justificación:** `AUD-064` registra que el permiso efectivo dependía del orden de resolución del cliente; un procedimiento fijado y comprobable por prueba elimina esa dependencia y hace verificable el menor privilegio de `AUD-061`.
- **Alternativas descartadas:** la última entrada coincidente gana, porque reproduce el defecto de `AUD-064` y hace que la posición en la lista decida el permiso; y la denegación absoluta sobre cualquier concesión, porque impediría al `coder` cerrar tareas en `specs/*/tasks.md` y anularía `RF-005`.

### DEC-002

- **Decisión:** la matriz declara cuatro acciones por rol —lectura, escritura, shell y subagentes—, con lectura concedida sobre `**` y `.env` denegado, y con denegación inicial de escritura, shell y subagentes. La allowlist de shell se escribe de forma literal por rol y el comodín de shell queda en `deny`.
- **Justificación:** `RF-001` exige declarar permisos por ruta, allowlist y política de subagentes; la forma tabular permitida por la lista de entradas es la única que el cliente interpreta y que una prueba puede contrastar sin ejecutar agentes.
- **Alternativas descartadas:** declarar los permisos en prosa dentro del cuerpo, porque no es contrastable; y una matriz única compartida por los seis roles, porque no expresa el menor privilegio que la constitución exige por función.

### DEC-003

- **Decisión:** el rol `auditor` se declara como subagente en `.opencode/agents/auditor.md`, con lectura de la base y de las specs, escritura limitada a `docs/sdd/auditoria_*.md`, shell de lectura y subagentes denegados, sin escritura sobre requisitos, código, configuración ni base normativa.
- **Justificación:** `AUD-063` registra que la función de auditoría se ejecutó con los permisos de documentación; un rol propio con escritura restringida por patrón cierra el hallazgo y permite al `documenter` conservar sus rutas sin ampliarlas.
- **Alternativas descartadas:** reutilizar `documenter` con una instrucción de alcance, porque mantiene el defecto; declarar el rol como primario, porque permitiría invocarlo directamente y ampliar su superficie de escritura.

### DEC-004

- **Decisión:** el flujo se dispara solo con `pull_request` dirigido a `dev` y a `main`, se ejecuta en `windows-latest` con Python 3.12, declara `contents: read`, ejecuta el validador y la suite en pasos separados, y fija cinco minutos para el trabajo y un minuto para la suite.
- **Justificación:** `RF-006`, `RF-007`, `RNF-001`, `RNF-002`, `RNF-007` y `RNF-008` fijan disparadores, ausencia de efectos remotos, entorno y umbrales; el disparador de Pull Request es el único que corresponde a la integración declarada en el flujo Git.
- **Alternativas descartadas:** disparar con `push`, porque ejecuta la verificación en ramas de trabajo sin solicitud de integración y duplica ejecuciones; usar `ubuntu-latest`, porque la plataforma objetivo es Windows y la suite verifica rutas de esa plataforma; y declarar una matriz de versiones de Python, porque triplica el tiempo sin aportar cobertura al contrato.

### DEC-005

- **Decisión:** las pruebas de configuración leen los archivos en modo texto, resuelven el permiso efectivo en memoria y comprueban la huella de los archivos antes y después. La regla de aprobaciones se verifica por dos vías: la declaración textual en el cuerpo del rol y la ausencia de concesión de escritura sobre `spec.md`, `CHANGELOG.md` y la sección de aprobaciones.
- **Justificación:** `RF-010` y `RNF-003` exigen una prueba no destructiva con umbral de 60 segundos; el parseo de texto satisface las dos condiciones y evita ejecutar el cliente de agentes.
- **Alternativas descartadas:** ejecutar los subagentes en un entorno aislado, porque es destructivo, lento y depende del cliente; y limitar la comprobación a la existencia de los archivos, porque no contrasta la matriz ni la precedencia.

### DEC-006

- **Decisión:** `AGENTS.md` recibe una modificación en sitio limitada al mapa de agentes y a la línea del rol de auditoría, con variación neta de tres líneas útiles como máximo; `MEMORY.md` actualiza la lista de agentes y añade la mención de la integración continua. Ningún otro cambio se aplica en esos documentos.
- **Justificación:** `RF-012`, `RF-013` y `AMB-005` fijan el alcance; `AGENTS.md` tiene 67 líneas útiles y el límite superior es 70, de modo que la variación neta debe quedar acotada.
- **Alternativas descartadas:** reescribir los documentos, porque altera reglas de la base y queda fuera de alcance; y dejar las menciones pendientes, porque conserva la desalineación de `AUD-091` y del mapa de agentes.

### DEC-007

- **Decisión:** el `documenter` escribe `AGENTS.md`; el orquestador redacta `.opencode/`, `opencode.jsonc`, `.github/` y `MEMORY.md` como delegado del propietario; el `coder` escribe `tools/sdd/tests/test_agent_permissions.py`. Cada escritura queda en el campo `Archivos` de su tarea.
- **Justificación:** el protocolo atribuye `AGENTS.md` al `documenter` y no atribuye configuración a rol alguno; la delegación del orquestador cubre la ruta sin permiso asignado y la conserva registrada, conforme a `AMB-005` y al límite de `DEC-003` del mecanismo.
- **Alternativas descartadas:** asignar la configuración al `coder`, porque la matriz del protocolo limita su escritura a `src/`, `tests/`, `tools/` y el cierre de tareas; y asignarla al `planner`, porque su escritura se limita a `specs/**`.

### DEC-008

- **Decisión:** el cierre de `AUD-081` a `AUD-084` y de `AUD-091` se registra en `validation_report.md` con una fila por hallazgo, el hecho acreditado, el comando literal y su resultado; una fila cuyo hecho no se acredita se escribe como abierta con el motivo.
- **Justificación:** `RF-008`, `RF-009` y `AMB-004` fijan el registro y la evidencia; el comando literal con su salida es la forma que el protocolo admite como evidencia verificable.
- **Alternativas descartadas:** declarar los cierres en el historial de cambios de la spec, porque mezcla el registro de versiones con la evidencia de práctica; y automatizar la comprobación en la suite, porque exigiría consultas al remoto y escrituras que la prueba no destructiva prohíbe.

### DEC-009

- **Decisión:** el módulo nuevo se descubre con el mismo comando de la suite, usa solo la biblioteca estándar, calcula la raíz con la ruta del propio archivo y no importa el módulo del validador. El validador y las 94 pruebas vigentes no se modifican.
- **Justificación:** `RNF-003`, `RNF-008` y la estrategia de la suite exigen una ejecución única de descubrimiento; mantener intacto el validador preserva el mecanismo de control de `SPEC-010` y evita mezclar dos contratos.
- **Alternativas descartadas:** añadir las pruebas al módulo del validador, porque mezcla la verificación del corpus con la del cliente de agentes; y añadir la comprobación al validador, porque modifica el mecanismo de control y pertenece a otra spec.

### DEC-010

- **Decisión:** el alcance se limita a los siete componentes declarados. No se modifica la base normativa, las specs publicadas, el validador, `src/`, `models/` ni `bin/`. El validador agregado devuelve cero antes y después del cambio, y la suite completa suma diecisiete pruebas a las 94 vigentes.
- **Justificación:** `AMB-007` prohíbe el cambio de la base y el informe asigna a esta spec solo el bloque B3; la comparación de `--all` y del recuento de pruebas demuestra que el cambio no introduce regresión.
- **Alternativas descartadas:** incorporar el enlace `CA → T` y la evidencia por tarea, porque pertenece al bloque B4; y reescribir los cinco roles vigentes en una sola pasada sin conservar sus descripciones, porque amplía el riesgo sin mejorar la verificabilidad.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Contraste de configuración | módulo `test_agent_permissions` sobre los seis roles | diecisiete pruebas en verde y cero conflictos de igual especificidad |
| Contraste de la configuración global | pruebas sobre `opencode.jsonc` | siete entradas declaradas, sin secreto literal y con la referencia al entorno |
| Estructura del flujo | pruebas sobre `.github/workflows/sdd.yml` | disparadores, ejecutor, versión, pasos y límites conformes |
| Documentación operativa | pruebas sobre `AGENTS.md` y `MEMORY.md` | longitud entre 30 y 70 líneas útiles y menciones completas |
| Validador del corpus | `python tools\sdd\validate.py --all` | `OK: sin hallazgos.` y código de salida 0 |
| Suite completa | `python -m unittest discover -s tools\sdd\tests -q` | 111 pruebas en verde y código de salida 0 |
| Evidencia de Git | cinco comandos de solo lectura registrados en el reporte | cada hallazgo cerrado con su hecho o abierto con su motivo |
| No regresión | huella de los artefactos de la base y de las specs publicadas | sin diferencia atribuible al cambio |

- La validación sigue el ciclo de prueba que falla, configuración mínima que la satisface y refactor con la suite en verde, aplicado a la configuración y al módulo de pruebas.
- No se produce script `.bat`, de modo que no aplica la declaración previa de comando, salida y métricas de la validación-first.
- La ejecución de la suite y del validador se documenta en el reporte de validación con su salida y su código de salida.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | Seis archivos de `.opencode/agents/` | `test_seis_roles_declarados`, `test_contrato_de_entrada_de_permiso` y `test_allowlist_de_shell` |
| `RF-002` | Procedimiento de resolución de la arquitectura | `test_especificidad_prevalece`, `test_denegacion_por_defecto` y `test_denegacion_prevalece_en_igual_especificidad` |
| `RF-003` | `.opencode/agents/auditor.md` | `test_auditor_solo_informes` y `test_auditor_no_aprueba` |
| `RF-004` | `.opencode/agents/reviewer.md` | `test_escritura_unica_del_reviewer` y `test_subagentes_por_rol` |
| `RF-005` | `.opencode/agents/coder.md` | `test_escritura_del_coder` |
| `RF-006` | `.github/workflows/sdd.yml` | `test_estructura_del_flujo` y ejecución local de los dos pasos con código de salida 0 |
| `RF-007` | `.github/workflows/sdd.yml` | `test_flujo_sin_efectos_remotos` |
| `RF-008` | Sección de cierre de práctica de `validation_report.md` | Revisión del reporte en G4 con las filas de `AUD-081` a `AUD-084` y su comando |
| `RF-009` | `MEMORY.md` y sección de cierre del reporte | `test_documentacion_operativa` y revisión de la fila de `AUD-091` |
| `RF-010` | `tools/sdd/tests/test_agent_permissions.py` | Ejecución del módulo con sus diecisiete pruebas y `test_prueba_no_destructiva` |
| `RF-011` | `opencode.jsonc` | `test_configuracion_global` |
| `RF-012` | `AGENTS.md` | `test_documentacion_operativa` con la mención del rol y la longitud |
| `RF-013` | `MEMORY.md` | `test_documentacion_operativa` con la lista de roles y la mención de la integración continua |
| `RNF-001` | Límite del trabajo en `.github/workflows/sdd.yml` | `test_estructura_del_flujo` y medición de la ejecución local de los dos pasos |
| `RNF-002` | Permisos del flujo | `test_flujo_sin_efectos_remotos` |
| `RNF-003` | `tools/sdd/tests/test_agent_permissions.py` | `test_prueba_no_destructiva` con huella de archivos y umbral de 60 segundos |
| `RNF-004` | Seis matrices de rol | `test_cero_conflictos_de_igual_especificidad` |
| `RNF-005` | `.opencode/agents/auditor.md` | `test_seis_roles_declarados` con la ruta única del rol |
| `RNF-006` | `opencode.jsonc` | `test_configuracion_global` con ausencia de secreto literal |
| `RNF-007` | Ejecutor y versión del flujo | `test_estructura_del_flujo` |
| `RNF-008` | Límite del paso de la suite | `test_estructura_del_flujo` |
| `CB-001` | Procedimiento de resolución | `test_denegacion_prevalece_en_igual_especificidad` |
| `CB-002` | Procedimiento de resolución | `test_denegacion_por_defecto` |
| `CB-003` | `.opencode/agents/auditor.md` | `test_auditor_solo_informes` |
| `CB-004` | `.opencode/agents/coder.md` | `test_escritura_del_coder` |
| `CB-005` | `.opencode/agents/reviewer.md` | `test_escritura_unica_del_reviewer` y `test_subagentes_por_rol` |
| `CB-006` | Pasos separados del flujo | `test_estructura_del_flujo` con dos pasos y ausencia de continuación en error |
| `CB-007` | `.github/workflows/sdd.yml` | `test_flujo_sin_efectos_remotos` |
| `CB-008` | Fila de `AUD-081` del reporte | Revisión de la fila con el comando de divergencia entre ramas |
| `CB-009` | Fila de `AUD-082` del reporte | Revisión de la fila con el listado de referencias |
| `CB-010` | Fila de `AUD-083` del reporte | Revisión de la fila con el listado de la rama y el registro de la decisión |
| `CB-011` | Fila de `AUD-084` del reporte | Revisión de la fila con el estado del árbol de trabajo |
| `CB-012` | Fila de `AUD-091` del reporte | `test_documentacion_operativa` y revisión de la fila con el contraste de hechos |
| `CB-013` | Modo declarativo del módulo de pruebas | `test_prueba_no_destructiva` con registro de comprobación no verificada cuando la ejecución exija escritura |
| `CB-014` | `.opencode/agents/auditor.md` | `test_auditor_no_aprueba` |
| `CB-015` | `.opencode/agents/auditor.md` | `test_auditor_solo_informes` con la ruta de `docs/sdd/` ajena al patrón |
| `CB-016` | Disparador del flujo | `test_estructura_del_flujo` con las dos ramas de destino |
| `CB-017` | Allowlist de shell de los seis roles | `test_allowlist_de_shell` |
