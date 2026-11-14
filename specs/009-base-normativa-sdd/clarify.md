# Clarificación — SPEC-009

## Estado

- [x] Cerrado (AMB resueltos y parches aplicados a `spec.md`).

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** RF-001 declaraba siete rangos, pero la spec no determinaba dónde se inscribe el mapa de autoridad ni qué documento prevalece cuando la contradicción ocurre entre dos documentos del mismo rango. RF-003 remitía al «orden de lectura declarado en el índice», y esa remisión admitía dos lecturas: un orden de lectura editorial sin efecto normativo, o un orden de precedencia con fuerza de desempate. Con la primera lectura, un conflicto entre documentos del mismo rango quedaba sin resolución y bloqueaba el trabajo sin salida.
- **Pregunta:** ¿En qué documentos se declara el mapa de autoridad y qué regla desempata una contradicción entre dos documentos del mismo rango?
- **Respuesta:** El mapa se declara en tres niveles: `docs/constitution.md` §6 fija la jerarquía suprema; `docs/sdd/PROTOCOLO_OPERATIVO.md` §2 la desarrolla con la tabla de rangos y carácter; `docs/sdd/README.md` la reproduce como índice de navegación. Para conflictos entre documentos del mismo rango, el índice declara el orden de precedencia dentro del rango y ese orden es el desempate.
- **Decisión:** Se reformula RF-003 con los tres niveles de declaración y con el orden de precedencia del índice como desempate dentro del rango, y se ajusta CA-002 a esa regla. La cobertura `RF-003` y `CB-001` se conserva.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** CB-005 impedía aprobar una compuerta cuando «el autor de la spec coincide con el actor que declara la aprobación». La redacción equiparaba dos figuras distintas: quien redacta el artefacto y quien lo aprueba. Bajo esa regla, el propietario quedaba impedido de aprobar cualquier spec que él mismo hubiera encargado y redactado por medio de un agente, y la comprobación dependía de una identidad declarada en un texto en lugar de una firma verificable.
- **Pregunta:** ¿Qué distingue al autor del propietario y qué evidencia convierte una línea de aprobación en compuerta aprobada?
- **Respuesta:** «Autor» es el agente o rol que redacta un artefacto; «propietario» es la persona que aprueba. La compuerta se aprueba solo si el commit que introduce la línea de aprobación está firmado por una clave de la lista de firmantes autorizados del propietario y la firma verifica.
- **Decisión:** Se reescribe CB-005 en términos de firma verificable del commit que introduce la línea de aprobación, se elimina la comparación entre autor de la spec y actor que declara la aprobación, y se ajusta CA-006 a la misma condición. La cobertura se conserva.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** RF-024 exigía registrar la transición desde la base vigente, pero no fijaba la relación entre los documentos sustituidos y los vigentes, ni la ubicación del registro, ni el destino de las versiones anteriores. Sin esa precisión, la publicación de la base v2 podía convivir con dos documentos vigentes en rutas distintas para la misma materia.
- **Pregunta:** ¿Qué relación tienen los documentos de la base v2 con los vigentes, dónde se registra la transición y qué ocurre con las versiones anteriores?
- **Respuesta:** Los documentos de la base v2 sustituyen a los vigentes en las mismas rutas: `docs/constitution.md`, `AGENTS.md`, `docs/sdd/PROTOCOLO_OPERATIVO.md`, `docs/Flujo_de_Trabajo_Git.md`, `README.md`, `MEMORY.md`, `docs/sdd/README.md` y `docs/sdd/plantillas/*`. Las versiones anteriores permanecen en el historial Git. El registro de transición se declara en un anexo del protocolo v2 y en `CHANGELOG.md` bajo `Unreleased`, con fecha, alcance y estado de cada documento sustituido.
- **Decisión:** Se amplía RF-024 con la regla de sustitución en la misma ruta, con la ubicación del registro y con la conservación de las versiones anteriores en el historial Git, y se ajusta CA-018.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** RF-019 declaraba un rol de auditoría con permisos delimitados y no fijaba dónde se declara ni quién lo implementa. La spec podía leerse como una autorización para crear un agente nuevo en `.opencode/`, materia que corresponde al bloque B3 del informe de auditoría y que excede el alcance declarado de esta spec.
- **Pregunta:** ¿Dónde se declara el rol de auditoría y qué alcance tiene su implementación dentro de esta spec?
- **Respuesta:** El rol se declara en la base v2, en el protocolo operativo v2 y en `AGENTS.md`. Su implementación en `.opencode/` corresponde a B3 y queda fuera de esta spec.
- **Decisión:** Se amplía RF-019 con los tres documentos de declaración y con la atribución de la implementación a B3, se añade la exclusión explícita en «Fuera de alcance» y se ajusta CA-012.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** RF-017 exigía cubrir «la totalidad de archivos presentes» y RF-018 prohibía fijar un recuento, pero no se enumeraba qué grupos de archivos entran en el índice. Un lector podía excluir los informes de análisis o el informe de auditoría por tratarse de documentación de proceso y dejar el índice incompleto sin incumplir la letra del requisito.
- **Pregunta:** ¿Qué archivos debe listar el índice de `docs/sdd/` y dónde se calcula el recuento del corpus?
- **Respuesta:** `docs/sdd/README.md` lista cada archivo de `docs/sdd/`, incluidos los de la raíz, los de `plantillas/`, los informes de análisis y el informe de auditoría, con su carácter y su orden de lectura. El recuento se calcula desde el índice y no se fija en ningún documento.
- **Decisión:** Se amplía RF-017 con los grupos de archivos cubiertos por el índice y se ajusta CA-014. RF-018 mantiene la prohibición de fijar un recuento.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** RF-016 exigía una regla de versionado «derivada del alcance del cambio» sin enumerar los incrementos ni el tratamiento de la reapertura y del estado `released`. Dos revisores podían derivar números distintos para el mismo cambio, y el historial de la propia spec no disponía de regla aplicable a la etapa de clarificación.
- **Pregunta:** ¿Qué incremento de versión corresponde a cada tipo de cambio y cómo se versiona la reapertura de una spec ya validada o publicada?
- **Respuesta:** Se adopta esta regla: 0.1.0 para la redacción inicial; incremento MINOR por cada etapa que cambie el contrato (clarify, plan, tasks y validación); incremento PATCH para correcciones editoriales que no cambien requisitos; reapertura tras `validated` con incremento MINOR y motivo registrado; una spec `released` no se renumera y cualquier cambio posterior se tramita por reapertura o por spec nueva.
- **Decisión:** Se amplía RF-016 con la regla completa, se ajusta CA-013 y se aplica la regla al historial de esta spec con la versión 0.2.0 tras la etapa de clarificación.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** RF-028 y CB-011 exigían registrar el archivo de la rama `feat/gemma-4-26b-a4b-it-qat-gguf` y excluirla de la integración, sin declarar la ubicación del registro ni el estado de publicación de la rama. La omisión dejaba abierta la posibilidad de publicar la rama en el remoto, decisión opuesta al archivo y no verificable por el criterio de aceptación.
- **Pregunta:** ¿Dónde se registra la decisión de archivo de la rama Gemma y cuál es su estado de publicación?
- **Respuesta:** La decisión se registra en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición del protocolo v2. La rama permanece local, no se publica y no se integra.
- **Decisión:** Se amplían RF-028 y CB-011 con la ubicación del registro y con el carácter local y no publicado de la rama, y se ajusta CA-019.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** El contexto afirmaba que «diecisiete documentos del corpus se autodeclaran no normativos». La cifra procede del corte de la auditoría y, leída como dato de la base v2, contradice RF-018, que prohíbe fijar un recuento y remite el inventario al índice. Un lector podía exigir que la base v2 conservara exactamente diecisiete documentos.
- **Pregunta:** ¿La cifra de diecisiete documentos describe la base v2 o solo el corte de la auditoría?
- **Respuesta:** La mención describe el corte de la auditoría y no fija un recuento para la base v2; el inventario vigente se calcula desde el índice.
- **Decisión:** Se añade una frase aclaratoria en «Contexto y objetivo» que acota la cifra al corte de la auditoría y remite el inventario a RF-018. No se modifica RF-018.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Sin casos borde nuevos. Cada decisión se inscribe en un caso existente: el desempate dentro del rango queda cubierto por CB-001, la aprobación sin firma verificable por CB-004 y CB-005, la sustitución en la misma ruta y la conservación en el historial Git por CB-003, el índice incompleto por CB-006 y CB-012, y el archivo de rama por CB-011.

## Parches aplicados a `spec.md`

- [x] Frontmatter: `status` actualizado a `clarified`, `version` incrementada a `0.2.0` y `updated` confirmado en 2026-11-14 (AMB-001 a AMB-008).
- [x] «Contexto y objetivo»: frase aclaratoria que acota la cifra de diecisiete documentos al corte de la auditoría y remite el inventario del corpus al índice (AMB-008).
- [x] RF-003: mapa de autoridad declarado en tres niveles y orden de precedencia del índice como desempate entre documentos del mismo rango (AMB-001).
- [x] RF-016: regla de versionado con 0.1.0 inicial, MINOR por etapa de contrato, PATCH editorial, reapertura de `validated` con motivo y prohibición de renumerar una spec `released` (AMB-006).
- [x] RF-017: enumeración de los grupos de archivos cubiertos por el índice, con los de la raíz, los de `plantillas/` y los informes de análisis y de auditoría (AMB-005).
- [x] RF-019: declaración del rol de auditoría en la base v2, el protocolo operativo v2 y `AGENTS.md`, con su implementación en `.opencode/` atribuida a B3 y fuera del alcance (AMB-004).
- [x] RF-024: sustitución en las mismas rutas, registro en el anexo del protocolo v2 y en `CHANGELOG.md` bajo `Unreleased`, y conservación de las versiones anteriores en el historial Git (AMB-003).
- [x] RF-028: registro de la decisión de archivo en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, con la rama local y no publicada (AMB-007).
- [x] CB-005: reescritura según la firma del commit que introduce la línea de aprobación, verificada contra la lista de firmantes autorizados del propietario, sin comparación entre autor y aprobador (AMB-002).
- [x] CB-011: registro del archivo en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, con la rama local y no publicada (AMB-007).
- [x] «Fuera de alcance»: exclusión explícita de la implementación del rol de auditoría en `.opencode/`, atribuida a B3 (AMB-004).
- [x] CA-002: resolución del conflicto por el orden de precedencia declarado dentro del rango, con `Cubre:` conservada en `RF-003` y `CB-001` (AMB-001).
- [x] CA-006: aprobación supeditada a firma verificable del commit que introduce la línea de aprobación, con `Cubre:` conservada en `RF-008`, `CB-004` y `CB-005` (AMB-002).
- [x] CA-012: declaración del rol de auditoría en los tres documentos y atribución de su implementación a B3, con `Cubre:` conservada en `RF-019` (AMB-004).
- [x] CA-013: incrementos MINOR y PATCH verificables en el historial de cambios, con `Cubre:` conservada en `RF-016` y `CB-013` (AMB-006).
- [x] CA-014: índice contrastado con los archivos de la raíz, de `plantillas/` y con los informes de análisis y de auditoría, con `Cubre:` conservada en `RF-017`, `RF-018`, `CB-006` y `CB-012` (AMB-005).
- [x] CA-018: consulta del anexo de transición y de `CHANGELOG.md` bajo `Unreleased`, con conservación de las versiones anteriores en el historial Git, y `Cubre:` conservada en `RF-024` (AMB-003).
- [x] CA-019: registro del archivo en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición, con la rama local y no publicada, y `Cubre:` conservada en `RF-028` y `CB-011` (AMB-007).
- [x] Historial de cambios: registro de la versión 0.2.0 tras la etapa de clarificación (AMB-001 a AMB-008).
- [x] `specs/INDEX.md`: fila de SPEC-009 actualizada al estado `clarified`.

## Decisiones de negocio

- El mapa de autoridad tiene un solo contenido y tres soportes: la constitución fija la jerarquía suprema, el protocolo la desarrolla y el índice la reproduce para navegación. Una divergencia entre soportes se corrige en el soporte de rango inferior.
- El índice del corpus adquiere una segunda función normativa: además de navegar, declara el orden de precedencia dentro de cada rango y ese orden es el desempate verificable entre documentos del mismo rango.
- La autoría no es un impedimento para la aprobación. Lo que convierte una línea de aprobación en compuerta aprobada es la firma del commit que la introduce, verificada contra la lista de firmantes autorizados del propietario.
- La base v2 se publica por sustitución en la misma ruta, no por convivencia de documentos paralelos. El historial Git es el archivo de las versiones anteriores y el anexo de transición más la entrada `Unreleased` de `CHANGELOG.md` son el registro consultable.
- El rol de auditoría se declara en esta spec y se implementa en B3: la declaración fija permisos y límites, y la creación del agente en `.opencode/` queda fuera del alcance.
- El recuento del corpus es un dato derivado del índice y nunca una constante documental; la cifra histórica de la auditoría se conserva como referencia de su corte.
- La rama `feat/gemma-4-26b-a4b-it-qat-gguf` permanece local, no se publica y no se integra; su archivo se registra en `CHANGELOG.md` bajo `Unreleased` y en el anexo de transición.
- La aprobación de G1 corresponde al propietario y se registra en un commit firmado; esta etapa no marca la casilla de la compuerta.
