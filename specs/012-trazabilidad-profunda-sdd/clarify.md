# Clarificación — SPEC-012

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-012` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `RF-004` y `RNF-008` exigían una evidencia «no vacía» de 20 caracteres o más sin fijar la unidad de conteo ni las cadenas que anulan el registro, de modo que una tarea podía cerrarse con un marcador sin sustituir y la comprobación quedaba al criterio de quien redacta.
- **Pregunta:** ¿Cuándo se considera registrada la evidencia de una tarea y qué cadenas la invalidan?
- **Respuesta:** la evidencia se considera registrada si, tras eliminar los espacios en blanco, tiene 20 caracteres o más y no coincide con una marca de pendiente. Las marcas de pendiente son `pendiente`, `N/A` y los términos vetados por el protocolo, entre ellos `TBD` y `por definir`; se citan como datos de la decisión y no como texto admitido en un requisito.
- **Decisión:** corrección de `RF-004` y de `RNF-008`, ajuste de `CB-004` y de `CA-004`. El umbral es determinista y se comprueba en el validador.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `RF-009` y `RNF-006` degradaban a advertencia las comprobaciones de una spec fuera del alcance declarado sin fijar el conjunto exacto ni la duración de la exención, de modo que la ventana podía ampliarse por conveniencia o quedar abierta de forma indefinida.
- **Pregunta:** ¿Qué specs quedan exentas de las comprobaciones nuevas y con qué límite?
- **Respuesta:** la regularización cubre `SPEC-001` a `SPEC-007`. `SPEC-008` a `SPEC-011` quedan exentas por ser posteriores al corte de la auditoría y estar validadas sin release. `SPEC-012` y las posteriores quedan sujetas a error. La exención se registra como cláusula de legado y no se amplía sin una spec posterior.
- **Decisión:** corrección de `RF-009` y de `RNF-006`, ajuste de `CB-010` y de `CA-012`, y entrada nueva en `## Fuera de alcance`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `RF-007` exigía regularizar las siete specs publicadas sin declarar el efecto sobre su versión ni la posición que se incrementa, mientras la regla de versionado distingue entre cambio de contrato, corrección editorial y reapertura.
- **Pregunta:** ¿Qué versión resulta de la regularización y qué se registra en el historial de cambios?
- **Respuesta:** la regularización incrementa la posición PATCH de cada spec e incorpora una fila de motivo en su historial de cambios. No cambia requisitos, criterios, comportamiento ni estado; solo añade los campos de trazabilidad. Un cambio que alterara un requisito sería MINOR y exigiría otra spec.
- **Decisión:** corrección de `RF-007` y de `CB-011`, caso borde nuevo `CB-017` y ajuste de `CA-010`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `RF-006` exigía declarar el commit de integración y el tag de release sin fijar la fuente de esos datos para las specs históricas, de modo que cada redactor podía elegir un valor distinto y la declaración no era contrastable.
- **Pregunta:** ¿De dónde proceden el commit de integración y el tag de release de las specs de `SPEC-001` a `SPEC-007`?
- **Respuesta:** se usan los merges y los tags registrados en el informe de auditoría y en el historial Git. Los valores son los de la tabla de `## Decisiones de negocio`. La regularización añade esos datos sin reescribir el contenido funcional.
- **Decisión:** corrección de `RF-007`, ajuste de `CA-009` y tabla de valores en `## Decisiones de negocio`. Sin caso borde nuevo: `CB-009` ya cubre la discrepancia entre el tag declarado y el registrado.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `RF-006` exigía declarar el merge y el tag «en el reporte de validación» sin fijar la sección ni la forma de la declaración, de modo que el dato podía quedar disperso en la matriz o en la sección de brechas y no era comprobable.
- **Pregunta:** ¿Dónde y con qué forma se declara el cierre de integración en el reporte de validación?
- **Respuesta:** el reporte incorpora una sección `## Cierre de integración` con las líneas `Merge:` y `Release:`. Una spec en `validated` o `released` sin esa sección produce error. Para las specs históricas los valores son los de `AMB-004`; para las nuevas, el merge de la integración y el tag del release cuando exista.
- **Decisión:** corrección de `RF-006`, caso borde nuevo `CB-016` y ajuste de `CA-007`. La alineación de la plantilla de rango 5 del reporte se registra como dependencia de una spec de base y se declara en `## Fuera de alcance`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `RF-005` exigía tratar como error el commit de implementación sin la cadena `Spec: SPEC-NNN` sin fijar el rango de commits examinados, de modo que la comprobación sobre el historial completo convertía en error los commits anteriores a la base v2.
- **Pregunta:** ¿Qué commits examina la comprobación de `Spec:` en la ejecución agregada?
- **Respuesta:** los commits posteriores al punto de integración de la rama actual o, en su defecto, los últimos 50. Los commits históricos sin `Spec:` quedan cubiertos por la ventana de legado y no convierten el corpus en error.
- **Decisión:** corrección de `RF-005`, caso borde nuevo `CB-018` y ajuste de `CA-005` y de `CA-006`.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `RF-001` exigía al menos un criterio de aceptación por tarea sin fijar la forma de declarar varios, ni el criterio de correspondencia recíproca entre criterio y tarea, de modo que una tarea con dos criterios admitía dos escrituras y el enlace `CA → T` no era determinista.
- **Pregunta:** ¿Cómo se declaran varios criterios en una tarea y qué correspondencia se exige?
- **Respuesta:** cada tarea declara al menos un `CA-NNN` existente en su criterio de aceptación y cada criterio tiene al menos una tarea. Un criterio sin tarea o una tarea con criterio inexistente produce error. Los criterios múltiples se enumeran separados por coma.
- **Decisión:** corrección de `RF-001`, caso borde nuevo `CB-015` y ajuste de `CA-001`. `RF-002` y `RF-003` ya fijan la doble dirección del enlace.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `RF-007` y `CB-013` describían la regularización como adición de campos sin declarar el conjunto de elementos que permanecen intactos, de modo que la frontera entre añadir trazabilidad y reescribir la spec publicada quedaba sin fijar.
- **Pregunta:** ¿Qué elementos de una spec publicada no se tocan al regularizarla?
- **Respuesta:** la regularización solo añade el criterio de aceptación y la evidencia a cada tarea, y la sección de cierre al reporte. No modifica requisitos, casos borde, criterios, tareas, estimaciones ni estados. La exención del historial de transiciones se conserva y no se añade fila de transición.
- **Decisión:** corrección de `RF-007`, ajuste de `CB-013`, de `CA-010` y de `## Fuera de alcance`. `CB-011` y `CB-014` conservan su vigencia.
- **Fecha:** 2026-11-14 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

### CB-015

`SI una tarea declara varios identificadores de criterio de aceptación sin separarlos por coma, ENTONCES la validación DEBE registrar un error de formato con el identificador de la tarea.`

### CB-016

`SI una spec en estado `validated` o `released` no declara la sección de cierre de integración, ENTONCES la validación DEBE registrar un error con el identificador de la spec.`

### CB-017

`SI una spec regularizada no incrementa la posición PATCH de su versión o no registra la fila de motivo en su historial de cambios, ENTONCES la validación DEBE registrar un error de versionado con el identificador de la spec.`

### CB-018

`SI un commit de implementación anterior al punto de integración de la rama no declara la cadena `Spec: SPEC-NNN`, ENTONCES la comprobación DEBE quedar cubierta por la ventana de legado y NO DEBE producir error.`

## Parches aplicados a `spec.md`

- [x] `RF-004` y `RNF-008`: umbral de 20 caracteres tras eliminar los espacios en blanco y lista de marcas de pendiente que anulan el registro — afecta a `RF-004`, `RNF-008`, `CB-004` y `CA-004`.
- [x] `RF-009` y `RNF-006`: ventana de legado limitada a `SPEC-008` a `SPEC-011`, registrada como cláusula de legado que no se amplía sin spec posterior, con error desde `SPEC-012` — afecta a `RF-009`, `RNF-006`, `CB-010` y `CA-012`.
- [x] `RF-007` y `CB-011`: incremento de la posición PATCH con fila de motivo en el historial de cambios, y trámite MINOR por spec nueva cuando el cambio altere un requisito — afecta a `RF-007`, `CB-011`, `CA-010` y caso borde nuevo `CB-017`.
- [x] `RF-007`: fuente histórica del commit de integración y del tag de release para las siete specs regularizadas — afecta a `RF-007` y a `CA-009`, con los valores en `## Decisiones de negocio`.
- [x] `RF-006`: sección `## Cierre de integración` con las líneas `Merge:` y `Release:`, y error por ausencia de la sección en una spec validada o publicada — afecta a `RF-006`, caso borde nuevo `CB-016` y `CA-007`.
- [x] `RF-005`: alcance de la comprobación de `Spec:` sobre los commits posteriores al punto de integración de la rama o los últimos 50, con la exención del historial anterior — afecta a `RF-005`, caso borde nuevo `CB-018`, `CA-005` y `CA-006`.
- [x] `RF-001`: enumeración de varios criterios separados por coma y error de formato cuando la separación falta — afecta a `RF-001`, caso borde nuevo `CB-015` y `CA-001`.
- [x] `CB-013` y `## Fuera de alcance`: conjunto de elementos intactos de la spec publicada y registro de la plantilla del reporte como dependencia de una spec de base — afecta a `RF-007`, `CB-013`, `CA-010` y `## Fuera de alcance`.
- [x] Casos borde nuevos `CB-015`, `CB-016`, `CB-017` y `CB-018` incorporados al cuerpo de la spec — afecta a `CB-015` a `CB-018`, `CA-001`, `CA-006`, `CA-007` y `CA-010`.
- [x] `## Contexto y objetivo` y `## Fuera de alcance`: el reporte declara el cierre en una sección propia y la plantilla de rango 5 se alinea en una spec de base — afecta a `RF-006` y a `RF-007`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-14 y `status` `clarified`; fila nueva en el historial de cambios y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- La evidencia de una tarea se acredita con la transcripción de la salida del comando que la cierra; la comprobación verifica presencia, longitud y ausencia de marca de pendiente, y no la veracidad del contenido.
- La ventana de legado es una concesión cerrada de cuatro specs: `SPEC-008` a `SPEC-011`. Una spec posterior se valida con las comprobaciones nuevas en calidad de error.
- La regularización es una corrección editorial: incrementa la posición PATCH, añade la fila de motivo y no altera el contrato funcional de la spec publicada.
- El estado y el historial de transiciones de las specs publicadas no se reescriben: la constancia de la regularización vive en el historial de cambios y la exención del historial histórico se conserva.

Valores históricos del cierre de integración:

| Spec | Commit de integración | Tag de release |
|---|---|---|
| `SPEC-001` | `753c3e5` | `v0.2.0` |
| `SPEC-002` | `ec6a063` | `v0.3.0` |
| `SPEC-003` | `39b27a2` | `v0.3.1` |
| `SPEC-004` | `b38ed6c` | `v0.4.0` |
| `SPEC-005` | `2781db5` | `v0.5.0` |
| `SPEC-006` | `0afc2ee` | `v0.5.1` |
| `SPEC-007` | `502c69d` | `v0.6.0` |

- Los valores de la tabla proceden del informe de auditoría y del historial Git; la regularización los transcribe en la sección de cierre de cada reporte y el validador contrasta el tag con el campo `release` del frontmatter y con la fila del índice.
- La sección de cierre es append-only: se añade sin alterar la matriz de trazabilidad ni el dictamen del reporte.
- La alineación de la plantilla de rango 5 del reporte con la sección de cierre queda como dependencia de una spec de base; mientras no se alinee, la sección se exige por esta spec y su comprobación no depende de la plantilla.
- La comprobación de `Spec:` no crea commits ni reescribe el historial: solo lee el historial local y no consulta el remoto.
- La trazabilidad declarada no acredita la conformidad del régimen ni sustituye la verificación del propietario en G1 ni en G4.
