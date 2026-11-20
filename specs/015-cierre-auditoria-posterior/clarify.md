# Clarificación — SPEC-015

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-015` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `AUD-087` acredita que el tag `v0.7.0` se recreó sobre el commit corregido y que la norma de rango 4 prohíbe mover, eliminar o reutilizar un tag publicado. El destino de la observación admitía dos sentidos opuestos: declarar el tag intocable sin procedimiento alguno o fijar un procedimiento de corrección con condiciones. Tampoco estaba fijado el identificador del tag anterior que la excepción debe registrar, ni si la corrección de un release publicado se tramita por etiqueta nueva o por nota de errata.
- **Pregunta:** ¿Se admite la corrección de un tag publicado, con qué condiciones y con qué registro, y cómo se cierra el desplazamiento ya ocurrido del tag `v0.7.0`?
- **Respuesta:** el tag publicado no se mueve y su corrección solo se admite con 3 condiciones simultáneas: autorización escrita del propietario, registro del identificador del tag anterior y ausencia de consumidores que dependan del tag. La corrección se ejecuta antes de que un consumidor dependa de la etiqueta; si un consumidor ya depende de ella, la corrección se tramita por un release PATCH nuevo con su propio tag. El caso `v0.7.0` se cierra como excepción registrada con el tag anterior `ad739a0` y el destino vigente `5a3af48`, queda declarada la deuda aceptada del release publicado y el tag no se mueve de nuevo.
- **Decisión:** requisito nuevo `RF-001`, con la tabla de condiciones habilitantes, y ajuste de `CB-001` y `CB-002` y de `CA-001`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `AUD-088` registra que el commit de empaquetado `5da6df6` modificó 18 archivos, entre ellos `MEMORY.md` y una suite de pruebas, sin tarea que lo declarara. La norma fija la rama de empaquetado, pero no enumera el alcance cerrado de sus artefactos ni el efecto de una ruta fuera de ese alcance.
- **Pregunta:** ¿Qué artefactos puede modificar la rama `release/vX-Y-Z` y qué ocurre cuando el empaquetado modifica una ruta distinta?
- **Respuesta:** la rama de empaquetado se limita a 4 artefactos: `CHANGELOG.md`, `specs/INDEX.md`, el frontmatter de las specs publicadas y la línea `Release:` de los reportes publicados. Cualquier otra ruta exige una spec previa o un fix previo con su tarea declarada; la verificación registra un error que nombra la ruta y el empaquetado no se declara conforme. El caso `v0.7.0` se registra como excepción con la regularización de la comprobación afectada y su fila en el registro de cambios.
- **Decisión:** requisito nuevo `RF-002`, con la tabla de artefactos admitidos, y ajuste de `CB-003` y de `CA-002`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `AUD-090` acredita que la entrada protegida del release recibió una modificación en un commit sin firma, después de la publicación. No estaba fijado si la corrección de una entrada publicada exige firma por cada modificación o solo en la primera, ni qué evidencia acredita la autoría.
- **Pregunta:** ¿Qué firma habilita la modificación de una entrada de release ya publicada y cómo se acredita?
- **Respuesta:** cada modificación posterior a la publicación de una entrada de release o de un artefacto de una spec publicada consta en 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados`, y el estado de firma del commit se transcribe en la evidencia del cierre. Una modificación sin firma verificable no se admite y su estado de firma se registra. La obligación no se satisface con la firma del commit de empaquetado original.
- **Decisión:** requisito nuevo `RF-003` y ajuste de `CB-004` y de `CA-003`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `AUD-089` registra que el reporte de `SPEC-014` declara el merge y la línea `Release:` y no transcribe el resultado de G6. El destino admitía corregir el reporte, corregir la entrada del release o añadir un registro nuevo en los dos soportes, y no estaba fijado si el registro puede alterar la matriz o el dictamen de una spec publicada.
- **Pregunta:** ¿En qué soporte y con qué forma se registra el resultado de G6 de un release ya publicado?
- **Respuesta:** se registra en el reporte de `SPEC-014` mediante una nota append-only que transcribe las 3 verificaciones de release: tag anotado verificado con su commit objetivo, `specs/INDEX.md` y `CHANGELOG.md` actualizados, y línea de G6 firmada. La nota no altera la matriz de trazabilidad ni el dictamen, conserva el estado `released` y no declara compuerta. La entrada del release conserva su línea de G6 y cualquier modificación posterior de ella queda sujeta a la firma de `RF-003`.
- **Decisión:** requisito nuevo `RF-004` y ajuste de `CB-005` y de `CA-004`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `AUD-076` registra que las filas `RNF-001` y `CA-015` de `SPEC-013` figuran en `PASADO` mientras la nota de cierre transcribe que su evidencia no acredita el valor literal `CONFORME` ni la cláusula de diez de diez dimensiones. El destino admitía corregir la fila, reabrir el criterio o registrar el valor efectivo sin tocar la matriz, y no estaba fijado qué significa resolver la evidencia diferida.
- **Pregunta:** ¿Cómo se resuelve la evidencia diferida de `RNF-001` y de `CA-015` sin reescribir el criterio publicado ni alterar la matriz?
- **Respuesta:** se añade una nota posterior append-only a la nota de cierre del reporte de `SPEC-013` que declara el valor efectivo de las 2 filas que la evidencia sostiene y registra el cierre de las 7 observaciones del informe final: 6 cerradas con artefacto y la séptima cerrada por esta spec. Las filas de la matriz y el dictamen `CONVERGIDO` conservan su contenido, el criterio publicado no se reescribe y ningún criterio se declara superado sin evidencia que lo sostenga.
- **Decisión:** requisito nuevo `RF-005` y ajuste de `CA-005`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `AUD-057` registra que la transición T7 de `SPEC-014` declara el tag pendiente de la firma de G6 mientras el release está publicado y la línea de G6 existe. No estaba fijado si la corrección se hace en la fila existente o en una fila nueva, ni cómo se versiona una spec publicada sin renumerarla.
- **Pregunta:** ¿Cómo se corrige la evidencia de T7 y qué efecto tiene sobre la versión de `SPEC-014`?
- **Respuesta:** se sustituye la evidencia de la fila T7 por el release publicado `v0.7.0` con el tag anotado verificado y la línea de G6 firmada, sin añadir una transición nueva. `SPEC-014` incrementa su versión en 1 incremento PATCH a 0.8.1 con 1 fila de motivo de regularización en su historial de cambios. El destino `released`, el campo `release`, los requisitos y los criterios se conservan y la spec no se renumera. Una corrección que altere el destino o el identificador del release se rechaza y el conflicto se registra en el reporte.
- **Decisión:** requisito nuevo `RF-006` y ajuste de `CB-006` y de `CA-006`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `AUD-039` registra que la fila G5 de la tabla de compuertas del rango 4 omite el check `verify` que el mismo documento declara exigible. No estaba fijado si la fila se amplía con la condición, si se corrige la regla de bloqueo o si la fila se remite a la regla ya declarada.
- **Pregunta:** ¿Qué forma toma la corrección de la fila G5 del rango 4?
- **Respuesta:** la fila incorpora el check `verify` a su condición, exigible con `strict: true` en `main` y en `dev`, y la regla de bloqueo del mismo documento se conserva sin cambio. La definición de la compuerta deja de ser más estrecha que la regla que la acompaña.
- **Decisión:** requisito nuevo `RF-007` y ajuste de `CA-007`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `AUD-068` registra que §12 del protocolo remite al bloque B3 para una formalización ya ejecutada por `SPEC-009` a `SPEC-012`. No estaba fijado si la remisión se elimina o se sustituye por una referencia vigente.
- **Pregunta:** ¿Qué texto sustituye la remisión al bloque B3?
- **Respuesta:** la remisión se sustituye por la referencia a la matriz de permisos vigente y a su formalización ejecutada, sin declarar pendiente una formalización que ya figura en la matriz y en §12. El rango del documento no cambia.
- **Decisión:** requisito nuevo `RF-008` y ajuste de `CA-007`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-009

- **Descripción:** `AUD-100` registra que el párrafo posterior al historial de releases declara en tiempo futuro una línea de G6 y una creación de tag ya ocurridas, y que la viñeta de la entrada describe el cierre con un rango de identificadores que incluye números no asignados. No estaba fijado el texto de reemplazo ni la enumeración de identificadores.
- **Pregunta:** ¿Qué texto reemplaza el párrafo y cómo se enumeran los identificadores de la viñeta?
- **Respuesta:** el párrafo declara en tiempo pasado la línea de G6 registrada en la entrada del release y la creación del tag `v0.7.0`. La viñeta enumera los 16 identificadores asignados que la entrada cita —`AUD-038`, `AUD-057`, `AUD-066`, `AUD-067`, `AUD-068`, `AUD-075`, `AUD-076`, `AUD-087`, `AUD-088`, `AUD-089`, `AUD-090`, `AUD-098`, `AUD-099`, `AUD-100`, `AUD-101` y `AUD-102`— en lugar del rango `AUD-038` a `AUD-102`, de modo que ningún número no asignado figura como cierre.
- **Decisión:** requisito nuevo `RF-009` y ajuste de `CA-007`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-010

- **Descripción:** `AUD-099` consta cerrada por la fila del informe en la tabla de inventario de `docs/sdd/README.md`, pero el informe posterior no declara su cierre y la spec podía exigir una modificación nueva de esa tabla. Tampoco estaba fijado cómo se computa una observación ya cerrada en el recuento de cierre.
- **Pregunta:** ¿Cómo se declara el cierre de `AUD-099` y qué evidencia lo sostiene?
- **Respuesta:** `AUD-099` se declara cerrada con la fila del informe en la tabla de inventario, que ya existe, y esta spec no modifica `docs/sdd/README.md`. El recuento de cierre del informe de la auditoría de `v0.7.1` es de 10 de 10, con `AUD-099` incluida y sin doble cómputo. Una observación sin artefacto de cierre no se declara cerrada y se registra como vigente.
- **Decisión:** requisito nuevo `RF-010` y ajuste de `CB-008` y de `CA-008`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-011

- **Descripción:** el cierre de las 10 observaciones requiere un release nuevo, y no estaba fijado el número de la versión, el soporte de la verificación ni el efecto del release sobre el tag `v0.7.0`. La norma permite un release PATCH sin incremento de contenido funcional, pero la corrección de un release publicado convivía con la prohibición de mover su etiqueta.
- **Pregunta:** ¿Cómo se publica el release que cierra las 10 observaciones y qué ocurre con el tag `v0.7.0`?
- **Respuesta:** se publica el release `v0.7.1` como incremento PATCH por el procedimiento de `docs/Flujo_de_Trabajo_Git.md`, con la verificación de G5 registrada, el tag anotado de mensaje `Release v0.7.1`, la línea de G6 firmada en su entrada de `CHANGELOG.md`, `specs/INDEX.md` y `CHANGELOG.md` actualizados y el informe de la auditoría de conformidad registrado. El tag `v0.7.0` conserva su destino `5a3af48` y no se mueve. Un tag existente detiene el procedimiento antes de crear la etiqueta y el identificador en conflicto se registra.
- **Decisión:** requisito nuevo `RF-011` y ajuste de `CB-007` y de `CA-009`, con los requisitos no funcionales `RNF-001` a `RNF-004` y sus criterios `CA-010` y `CA-011`.
- **Fecha:** 2026-11-20 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

Sin casos borde nuevos en esta clarificación: los 8 casos borde de `spec.md` se redactaron en la versión 0.1.0 y esta clarificación ajusta su redacción en los puntos que `AMB-001`, `AMB-002`, `AMB-003`, `AMB-004`, `AMB-006`, `AMB-010` y `AMB-011` fijan.

## Parches aplicados a `spec.md`

- [x] `RF-001` con la tabla de las 3 condiciones habilitantes, el registro del identificador anterior y la excepción del caso `v0.7.0` con el tag anterior `ad739a0` y el destino `5a3af48` — afecta a `RF-001`, `CB-001`, `CB-002` y `CA-001`.
- [x] `RF-002` con la tabla de los 4 artefactos admitidos en la rama de empaquetado, la exigencia de spec previa o de fix previo y la excepción del caso `v0.7.0` — afecta a `RF-002`, `CB-003` y `CA-002`.
- [x] `RF-003` con la exigencia de 1 commit firmado por una clave de `docs/sdd/firmantes_autorizados` para cada modificación posterior a la publicación y la transcripción del estado de firma — afecta a `RF-003`, `CB-004` y `CA-003`.
- [x] `RF-004` con la nota append-only del resultado de G6 en el reporte de `SPEC-014` y las 3 verificaciones transcritas, sin alterar matriz ni dictamen — afecta a `RF-004`, `CB-005` y `CA-004`.
- [x] `RF-005` con la nota posterior append-only del reporte de `SPEC-013`, el valor efectivo de `RNF-001` y de `CA-015` y el cierre de las 7 observaciones del informe final — afecta a `RF-005` y `CA-005`.
- [x] `RF-006` con la evidencia de T7 del release publicado, el incremento PATCH a 0.8.1 de `SPEC-014` y la fila de motivo de regularización — afecta a `RF-006`, `CB-006` y `CA-006`.
- [x] `RF-007`, `RF-008` y `RF-009` con las 3 correcciones de alineación, la enumeración de los 16 identificadores asignados y la tabla de trazabilidad con el destinatario de cada una — afecta a `RF-007`, `RF-008`, `RF-009` y `CA-007`.
- [x] `RF-010` con el cierre de las 10 observaciones por artefacto y evidencia, `AUD-099` cerrada por la fila del inventario y el recuento de 10 de 10 — afecta a `RF-010`, `CB-008` y `CA-008`.
- [x] `RF-011` con el release `v0.7.1` por el procedimiento vigente, el tag anotado y la conservación del tag `v0.7.0` — afecta a `RF-011`, `CB-007` y `CA-009`.
- [x] `RNF-001` a `RNF-004` con el recuento de filas de matriz y de dictámenes alterados, la forma del tag `v0.7.1`, el límite de 300 segundos de la validación agregada y la conservación de los requisitos publicados — afecta a `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004`, `CA-010` y `CA-011`.
- [x] `## Actores y permisos` con la autorización escrita del propietario, la firma de cada modificación publicada, la delegación de las notas append-only al `reviewer` y las competencias del `coder` y del `documenter` — afecta a `RF-001`, `RF-003`, `RF-004` y `RF-005`.
- [x] `## Fuera de alcance` con la conservación del tag `v0.7.0`, la prohibición de reescribir historia publicada, el cierre previo de `AUD-099` y la ausencia de declaración de compuertas — afecta a `RF-001`, `RF-010` y `RF-011`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-20 y `status` `clarified`; fila nueva en `## Historial de cambios` y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- El tag publicado no se repara moviéndolo: la reparación es declarativa, con el procedimiento escrito, el registro del identificador anterior y el release que corresponde al contenido publicado. El desplazamiento ya ocurrido del tag `v0.7.0` se registra como deuda aceptada y no se repite.
- El alcance de la rama de empaquetado es una lista cerrada de 4 artefactos y no una recomendación. La modificación de una ruta fuera de esa lista es una modificación de contenido y exige su propia spec o su propio fix, con tarea declarada y evidencia.
- La firma del propietario es el único medio admitido para modificar un artefacto publicado, y la firma del empaquetado no se extiende a las correcciones posteriores a la publicación.
- Las notas append-only son el mecanismo de corrección de un reporte publicado: registran el resultado observado y no reescriben la fila, la matriz ni el dictamen que ya se publicaron.
- La evidencia diferida de `RNF-001` y de `CA-015` se resuelve declarando el valor efectivo que la evidencia sostiene. El criterio publicado no se reescribe para acomodarlo a la evidencia ni la evidencia se ajusta al criterio.
- Una spec publicada se corrige con incremento PATCH y fila de motivo de regularización, sin renumeración y sin reescritura de sus requisitos ni de sus criterios.
- La alineación de una definición de compuerta no altera la regla que esa definición acompaña: se corrige la omisión y se conserva la norma.
- El recuento de cierre es explícito por observación. Una observación ya cerrada se declara con su artefacto y no se computa dos veces; una observación sin artefacto permanece vigente.
- El release `v0.7.1` es un incremento PATCH que cierra la auditoría posterior y no incorpora contenido funcional nuevo.
- El validador acredita estructura, coherencia y trazabilidad declarada; no acredita la veracidad de la evidencia transcrita, la ejecución real del flujo ni la conformidad del régimen, y no sustituye la firma del propietario en G1 ni en G4.
