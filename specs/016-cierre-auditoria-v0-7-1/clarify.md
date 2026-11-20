# Clarificación — SPEC-016

*Artefacto de rango 6: registro de las ambigüedades de `SPEC-016` resueltas con el propietario antes de abrir Plan. Al cierre no queda ninguna casilla pendiente: el cierre sin casillas abiertas es condición de G1.*

## Hallazgos de ambigüedad

### AMB-001

- **Descripción:** `AUD-109` acredita que `RF-010` y `CA-008` de `SPEC-015` fijaron como condición que el informe de auditoría de `v0.7.1` declarara «10 de 10 cerradas», y que `RNF-001` y `CA-015` de `SPEC-013` fijaron el veredicto `CONFORME` de la auditoría de cierre. El destino de la observación admitía tres sentidos: corregir las 2 specs afectadas, prohibir la forma solo hacia adelante o prohibir la forma y regularizar lo ya publicado. Tampoco estaba fijado si la prohibición alcanza al veredicto, al recuento de hallazgos, al conjunto de dimensiones o a la existencia del informe.
- **Pregunta:** ¿Qué puede exigir un requisito o un criterio de aceptación de una spec cuando invoca una auditoría de conformidad posterior a su aprobación?
- **Respuesta:** una spec no fija el veredicto, el recuento de hallazgos ni el conjunto de dimensiones de un informe que se emite después de su aprobación. El criterio se limita a exigir la existencia del artefacto de auditoría y la evidencia transcrita por ruta y línea. El veredicto y el recuento los emite el rol de auditoría, de modo que la compuerta que se apoya en ese informe conserva evidencia independiente del objeto auditado. La prohibición se declara en §16 del protocolo operativo y en la lista de prohibiciones de la plantilla de `spec.md`, y un criterio que fije el veredicto o el recuento se registra como hallazgo y no obtiene G1.
- **Decisión:** requisito nuevo `RF-001`, caso borde `CB-006` y criterio `CA-001`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-002

- **Descripción:** `AUD-109` deja abierta la suerte de las 2 specs publicadas que ya portan la forma prohibida. La prohibición hacia adelante no corrige `SPEC-013` ni `SPEC-015`, y no estaba fijado si se reescriben el requisito y el criterio publicados, si se reabren las specs o si se corrige el efecto con una nota sin tocar el texto publicado.
- **Pregunta:** ¿Cómo se regularizan las 2 specs publicadas que ya fijan el veredicto o el recuento, sin reescribir lo publicado ni renumerar la spec?
- **Respuesta:** se añade a cada reporte de validación 1 nota append-only que transcribe la regla, declara que el veredicto y el recuento los emite el rol de auditoría y declara que el criterio publicado se lee como exigencia del artefacto y de su evidencia. Cada spec incrementa 1 incremento PATCH hasta su versión resultante con 1 fila de motivo por corrección. El requisito, el criterio, la matriz y el dictamen conservan su texto, la spec conserva `status: released` y su campo `release`, y ningún criterio se declara superado. La modificación de esos artefactos publicados consta en un commit firmado por el propietario.
- **Decisión:** requisito nuevo `RF-002` con la tabla de las 2 specs afectadas y criterio `CA-002`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-003

- **Descripción:** `AUD-103` y el residuo de `AUD-088` registran que §15 del rango 3 enumera 3 artefactos de la rama `release/vX-Y-Z`, que el paso 3 del rango 4 enumera 4 y que el empaquetado de `v0.7.1` escribió además la fila del historial de cambios y la fila T7 de `SPEC-015`. No estaba fijado el conjunto único, ni el orden de corrección entre los 2 rangos, ni el efecto de una enumeración divergente.
- **Pregunta:** ¿Qué conjunto de artefactos admite la rama de empaquetado y en qué orden se corrigen los 2 documentos?
- **Respuesta:** el conjunto es único y consta de 6 artefactos: la entrada del release y el historial de releases de `CHANGELOG.md`; la fila de la spec publicada en `specs/INDEX.md`; los campos del frontmatter de la spec publicada; la fila del historial de cambios de la versión de release; la fila T7 del historial de transiciones; y la línea `Release:` del reporte publicado. El rango 3 se escribe antes que el rango 4 por el orden de precedencia. Cualquier ruta distinta exige una spec previa o un fix previo, y una divergencia entre las 2 enumeraciones produce un error que la nombra y no se declara alineada.
- **Decisión:** requisito nuevo `RF-003` con la tabla de los 6 artefactos, caso borde `CB-003` y criterio `CA-003`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-004

- **Descripción:** `AUD-104` y el residuo de `AUD-090` registran que el commit `564bac4`, sin firma verificable, modificó la entrada publicada `v0.7.0` de `CHANGELOG.md`, la fila T7 de `SPEC-014` y la nota del reporte de `SPEC-013`, y que ese mismo commit introdujo la regla que exige firma para cada modificación posterior a la publicación. El destino admitía revertir el contenido, reescribir el historial o ratificar las modificaciones con un acto firmado. No estaba fijado el contenido del registro, su ubicación ni el efecto de la ratificación sobre el contenido publicado.
- **Pregunta:** ¿Cómo se cierra la modificación sin firma de artefactos publicados sin reescribir el contenido ni el historial?
- **Respuesta:** se registra 1 ratificación del propietario en un commit firmado con una clave de `docs/sdd/firmantes_autorizados`. La ratificación se declara en la entrada `Unreleased` de `CHANGELOG.md` con el identificador `564bac4`, las 3 rutas publicadas que modificó, la fecha, el alcance y su efecto declarativo: el contenido publicado se conserva y la autoría queda acreditada por la firma del acto de ratificación. El estado de firma y la huella de la clave se transcriben en la evidencia de cierre. Una ratificación sin firma verificable no se admite.
- **Decisión:** requisito nuevo `RF-004` con el cierre del caso `564bac4`, caso borde `CB-002` y criterio `CA-004`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-005

- **Descripción:** `AUD-105` y el residuo de `AUD-089` registran que la entrada del release `v0.7.1` porta la línea de aprobación y el bloque de cambios sin el resultado de G5 ni el de G6, y que el reporte de `SPEC-015` anuncia una transcripción del objeto del tag que no existe en el documento publicado. Los 2 soportes de §13 quedan incompletos y no estaba fijado si se corrige el reporte, la entrada o ambos, ni si la transcripción puede alterar la matriz, el dictamen o la línea de aprobación.
- **Pregunta:** ¿En qué soportes y con qué forma se registra el resultado de G5 y de G6 y el objeto del tag de un release ya publicado?
- **Respuesta:** en los 2 soportes que §13 exige. El reporte de `SPEC-015` recibe 1 nota append-only con el resultado de G5 y de G6 y con el objeto anotado del tag `v0.7.1`, su mensaje y su commit objetivo. La entrada `v0.7.1` de `CHANGELOG.md` recibe 1 bloque de registro con ese mismo contenido. La matriz de trazabilidad, el dictamen y la línea de aprobación de G6 conservan su texto, una transcripción previa del objeto se conserva y la nota nueva se añade a continuación, y ninguna de las 2 escrituras declara compuerta.
- **Decisión:** requisito nuevo `RF-005`, caso borde `CB-005` y criterio `CA-005`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-006

- **Descripción:** `AUD-108` registra que las 2 filas T7 declaran el tag «verificado sobre el commit de empaquetado», mientras los tags apuntan a los commits de merge publicados en `main` y los commits de empaquetado son sus ancestros. No estaba fijado si la corrección añade una fila nueva, si sustituye la evidencia de la fila existente ni qué identificador debe declarar la fila.
- **Pregunta:** ¿Cómo se corrige la redacción de las 2 filas T7 y qué identificador debe declarar cada una?
- **Respuesta:** se sustituye la evidencia de la fila existente de cada spec, sin añadir una transición nueva. Cada fila declara que el tag anotado apunta al commit de merge publicado en `main`, con su identificador y su relación de ancestría con el commit de empaquetado. Las 2 specs conservan `status: released`, su campo `release` y el identificador del release, e incrementan 1 incremento PATCH con 1 fila de motivo por corrección. Una corrección que altere el destino, el campo `release` o el identificador del release se rechaza y el conflicto se registra en el reporte de la spec afectada.
- **Decisión:** requisito nuevo `RF-006`, caso borde `CB-004` y criterio `CA-006`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-007

- **Descripción:** `AUD-110` registra que la fila 34 de la tabla de inventario de `docs/sdd/README.md` se escribió en un commit sin firma, en el mismo commit que el informe `docs/sdd/auditoria_posterior_v0_7_0.md`, fuera del alcance de escritura del rol de auditoría. No estaba fijado qué rol escribe la fila, en qué momento respecto de la integración del informe ni qué ocurre cuando la fila falta.
- **Pregunta:** ¿Qué rol escribe la fila de inventario de un informe de auditoría y en qué momento?
- **Respuesta:** la fila la escribe el `documenter` antes de integrar el informe, con la misma solución estructural que la fila del informe `v0.7.0`. El rol de auditoría conserva la escritura limitada al informe que produce y no escribe la fila. El cauce se declara en §12 del protocolo y en la sección de inventario de la plantilla de informe de auditoría. La fila 34 se conserva y su escritura se atribuye a la sesión del propietario, no al rol de auditoría. Un informe integrado sin fila deja el check `verify` en rojo con la ruta del archivo sin fila y detiene la integración.
- **Decisión:** requisito nuevo `RF-007`, caso borde `CB-007` y criterio `CA-007`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-008

- **Descripción:** `AUD-106` y `AUD-107` figuran corregidos: el listado de ramas locales ya no conserva las 2 ramas de empaquetado y la tabla de inventario ya porta la fila del informe `docs/sdd/auditoria_final_v0_7_1.md`. No estaba fijado cómo se registra el cierre de una observación que se corrigió antes de la redacción de esta spec, ni qué evidencia lo sostiene.
- **Pregunta:** ¿Cómo se declara el cierre de 2 observaciones cuya corrección ya ocurrió antes de esta spec?
- **Respuesta:** se registra el cierre con la evidencia transcrita en el commit validado: el listado de ramas locales sin `release/v0-7-0` ni `release/v0-7-1` y la fila del informe con el número de fila que la tabla declara, junto con el resultado de la suite de pruebas del corpus. Una observación cuyo artefacto o cuya evidencia falte no se declara cerrada y su causa figura como vigente.
- **Decisión:** requisito nuevo `RF-008`, caso borde `CB-001` y criterio `CA-008`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-009

- **Descripción:** el cierre de 11 observaciones de 5 clases distintas exige un registro por observación, y no estaba fijado si el cierre se acredita con el informe de una auditoría posterior o con el artefacto de cada observación, ni si esta spec puede declarar conformidad del régimen al cerrar sus observaciones.
- **Pregunta:** ¿Con qué se acredita el cierre de las 11 observaciones y qué declara esta spec sobre la conformidad del régimen?
- **Respuesta:** con 1 fila por observación en la tabla de cierre, con el artefacto que la cierra y la evidencia transcrita por ruta y línea. El estado cerrado figura solo en las filas cuyo artefacto consta en el commit validado. El cierre no depende de un informe de auditoría posterior: la auditoría de una spec no puede ser condición de su propio cierre. Esta spec no declara veredicto ni conformidad del régimen; el veredicto lo emite el rol de auditoría en su informe.
- **Decisión:** requisito nuevo `RF-009`, caso borde `CB-001` y criterio `CA-009`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-010

- **Descripción:** el residuo de `AUD-088` registra que la comprobación del historial de releases compara el número de filas con el número de encabezados y que la constante que admite el estado `released` conserva la forma anterior, sin cambio posterior al commit `5da6df6` y sin fila que lo describa en el registro de cambios. No estaba fijado si la comprobación se regulariza, si se declara la regla más estrecha o si se acepta el defecto como deuda.
- **Pregunta:** ¿Cómo se cierra el residuo de `AUD-088` sobre la comprobación del historial de releases?
- **Respuesta:** se regulariza la comprobación para que admita las filas de historial de cambios y de transición que el empaquetado escribe y la constante de estados que admite `released`, y la regularización consta en 1 fila del registro de cambios bajo `Unreleased`. Ninguna comprobación se declara conforme con una regla más estrecha que el alcance de 6 artefactos. La regularización se escribe en `tools/` con la tarea declarada y con la salida de la suite transcrita.
- **Decisión:** requisito nuevo `RF-010` y criterio `CA-010`, con los requisitos no funcionales `RNF-001` a `RNF-004` y su criterio `CA-011`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-011

- **Descripción:** los 5 informes de `docs/sdd/` emitieron hallazgos con identificador `AUD-NNN` y el corpus no conserva un registro único de su estado: cada informe declara el estado en su propia tabla y el vocabulario diverge entre `CERRADO`, `CERRADO POR EXENCIÓN`, `PARCIAL` y `VIGENTE`. No estaba fijado el soporte del registro, sus campos, el vocabulario admitido del estado, el rol que escribe la fila ni el efecto de un hallazgo sin fila.
- **Pregunta:** ¿En qué soporte se registra el estado de cada hallazgo, con qué campos, con qué vocabulario y con qué rol como escritor?
- **Respuesta:** un inventario único en `docs/sdd/inventario_hallazgos.md` con 1 fila por hallazgo y 8 campos: identificador, dimensión, severidad, informe de origen, regla normativa citada, estado, evidencia de cierre e informe que declara el estado. El vocabulario del estado es cerrado en 5 valores: `cerrado`, `parcial`, `vigente`, `cerrado por exención` y `cerrado por ratificación`. El identificador se conserva sin reutilización ni renumeración, y un estado posterior se anota sobre la misma fila con el informe que lo declara. Las filas las escribe el `documenter` antes de integrar el informe, con el mismo cauce que la fila de la tabla de inventario del corpus; el rol de auditoría no escribe la fila. Un informe integrado sin fila o un hallazgo sin fila deja la verificación en rojo con la ruta del archivo y detiene la integración.
- **Decisión:** requisito nuevo `RF-011` con la tabla de los 8 campos, casos borde `CB-008` y `CB-013` y criterio `CA-012`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-012

- **Descripción:** el informe de `v0.7.1` computa como hallazgo juicios de forma, de redacción y de autoría, y su recuento depende del criterio de cada pasada. La plantilla de rango 5 exige evidencia citada por ruta y sección, y no fija la regla que separa un hallazgo de una observación ni el efecto de la observación sobre el veredicto.
- **Pregunta:** ¿Qué distingue un hallazgo de una observación y cómo computa cada uno en el veredicto?
- **Respuesta:** un hallazgo cita la regla normativa que se incumple con su ruta, su capítulo y su línea. El juicio que no cita una regla se registra como observación, queda fuera del recuento de hallazgos y su severidad no computa como hallazgo abierto. La observación de severidad `Alta` o `Media` impide el veredicto `CONFORME` mientras carezca de tratamiento, y la de severidad `Baja` no lo impide. Un tratamiento es la decisión registrada del propietario, con fecha e identificador del commit, que declara el efecto de la observación y su destino.
- **Decisión:** requisito nuevo `RF-012`, caso borde `CB-009` y criterio `CA-013`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-013

- **Descripción:** cada informe aplicó una regla propia al veredicto de dimensión y el veredicto global se derivó de esos veredictos y no de un recuento de filas. El estado de un hallazgo quedó así separado del veredicto que sostiene, y no estaba fijado si el veredicto se calcula desde el inventario, cuál es su precedencia ni qué exige el valor `CONFORME`.
- **Pregunta:** ¿Cómo se calcula el veredicto de auditoría y qué exige el valor `CONFORME`?
- **Respuesta:** el veredicto se calcula desde el estado de las filas del inventario con una tabla de 4 condiciones: `NO CONFORME` con 1 o más hallazgos abiertos de severidad `Crítica` o `Alta`; `NO VERIFICABLE` con 0 de esas severidades y 1 o más filas sin regla citada o sin evidencia de cierre; `PARCIAL` con 0 filas sin regla o sin evidencia y 1 o más hallazgos abiertos de severidad `Media` o `Baja`, o 1 o más observaciones de severidad `Alta` o `Media` sin tratamiento; y `CONFORME` con 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. La precedencia es `NO CONFORME`, después `NO VERIFICABLE`, después `PARCIAL` y después `CONFORME`. Un veredicto que contradiga el recuento se registra como error con la fila que sostiene la diferencia.
- **Decisión:** requisito nuevo `RF-013` con la tabla de condiciones, caso borde `CB-010` y criterio `CA-014`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-014

- **Descripción:** el corpus conserva 5 hallazgos con estado `CERRADO POR EXENCIÓN` —`AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053`— y 2 modificaciones de artefactos publicados en commits sin firma verificable —`494db2e` y `564bac4`—. Ningún artefacto repara la causa de esos casos sin reescribir contenido publicado o historia integrada, y no estaba fijado el instrumento de cierre, su alcance ni el efecto retroactivo que produce.
- **Pregunta:** ¿Con qué instrumento se cierran las violaciones históricas que ningún artefacto repara y qué efecto tiene ese cierre?
- **Respuesta:** con 1 ratificación firmada del propietario con una clave de `docs/sdd/firmantes_autorizados`. La ratificación declara el alcance, la fecha, las rutas o los identificadores afectados y el efecto retroactivo limitado al régimen: la autoría queda acreditada por la firma del acto, el contenido publicado y el informe de origen conservan su texto, y ninguna regla ajena al régimen queda alcanzada. La fila del inventario pasa a `cerrado por ratificación` con el identificador del commit. `RF-004` registra la ratificación del commit `564bac4` y `RF-014` declara el efecto común sobre los 7 casos; una ratificación sin firma verificable no se admite.
- **Decisión:** requisito nuevo `RF-014`, caso borde `CB-011` y criterio `CA-015`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-015

- **Descripción:** el informe de `v0.7.1` declara el veredicto `NO CONFORME` y el rango 4 desplaza la corrección de un release publicado a un release PATCH. El rango 3 exige una auditoría antes de cada release menor y no fija la condición de un release PATCH posterior a un veredicto no conforme, ni el momento de la auditoría respecto de la integración, ni la secuencia con G5 y G6.
- **Pregunta:** ¿Con qué condición y en qué orden se publica el release v0.7.2?
- **Respuesta:** la auditoría se ejecuta sobre el estado integrado en `dev`, después de la integración de esta spec y antes del empaquetado, y el release se publica solo si el veredicto es `CONFORME` conforme a `RF-013`. La entrada del release transcribe el identificador del informe y el veredicto. La secuencia es G5, después auditoría sobre el estado integrado, después G6. Un veredicto distinto de `CONFORME` impide la publicación, conserva la spec en `validated` y transcribe el motivo con el hallazgo que lo sostiene.
- **Decisión:** requisito nuevo `RF-015`, caso borde `CB-012` y criterio `CA-016`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-016

- **Descripción:** `AUD-103`, `AUD-105`, `AUD-108`, `AUD-110` y los parciales `AUD-088` y `AUD-089` tienen su causa en artefactos que esta spec escribe, y no estaba fijado el artefacto de cierre de cada uno ni la evidencia que lo sostiene. La emisión de un informe de auditoría posterior no es evidencia admisible de cierre, porque ese informe evalúa la spec y no puede ser condición de su propio cierre.
- **Pregunta:** ¿Con qué artefacto y con qué evidencia se cierra cada uno de esos 6 hallazgos?
- **Respuesta:** `AUD-103` se cierra con la enumeración única de 6 artefactos de empaquetado en el rango 3 y en el rango 4; `AUD-105` y `AUD-089` con la nota append-only del reporte publicado y el bloque de registro de la entrada del release, con el resultado de G5 y de G6 y el objeto del tag; `AUD-108` con la corrección de las 2 filas T7 al commit de merge publicado; `AUD-110` con el cauce del `documenter` para la fila de inventario y la atribución de la fila 34; y `AUD-088` con la regularización de la comprobación del historial de releases y su fila en el registro de cambios. Cada cierre exige la evidencia transcrita por ruta y línea en el commit validado, y un hallazgo sin artefacto permanece vigente.
- **Decisión:** `RF-003`, `RF-005`, `RF-006`, `RF-007` y `RF-010` con `CA-003`, `CA-005`, `CA-006`, `CA-007` y `CA-010`; `RF-011` a `RF-015` con `RNF-005` a `RNF-009` y `CA-012` a `CA-017`.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-017

- **Descripción:** la auditoría previa al release v0.7.2 emitió el hallazgo `H-01` y registró en §9 que el inventario no admite sus filas porque `RF-011` limita el alcance a los 5 informes de `docs/sdd/` con los que se redactó el inventario. El corpus conserva informes integrados con posterioridad, de modo que el recuento de `RF-013` no alcanza los hallazgos de un informe nuevo y el veredicto calculado no cubre el estado auditado.
- **Pregunta:** ¿Qué informes alcanza el inventario de hallazgos?
- **Respuesta:** el inventario cubre los informes de auditoría presentes en `docs/sdd/`, sin límite de cinco ni enumeración cerrada. El alcance de `RF-011` queda definido por la ubicación del archivo y no por la fecha de corte del inventario, la comprobación recorre cada informe presente y un informe integrado sin fila detiene la integración conforme a `CB-013`. La ampliación del inventario no reescribe los informes publicados ni los cita como modificados.
- **Decisión:** parche a `RF-011` y al párrafo de la ampliación del contrato que enumeraba los 5 informes.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-018

- **Descripción:** `RF-015` y `CA-016` exigían que la auditoría previa al release v0.7.2 declarara el veredicto `CONFORME`, y `RNF-009` y `CB-012` repetían esa condición. `§16` del protocolo prohíbe que una spec fije el veredicto de un informe emitido después de su aprobación, de modo que el requisito anulaba la independencia de la evidencia y contradecía el recuento nulo de `RNF-001`. `CA-017` acreditaba ese recuento en 0.
- **Pregunta:** ¿Qué condición sustituye la exigencia del veredicto `CONFORME` en el contrato del release v0.7.2?
- **Respuesta:** la condición se expresa sobre el inventario y no sobre el veredicto: 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. `RF-015`, `RNF-009`, `CB-012` y `CA-016` dejan de nombrar los valores del veredicto; la entrada del release transcribe el identificador del informe y el recuento de hallazgos abiertos; `RF-013` conserva el cálculo del veredicto como definición normativa aplicable a cualquier corte y no como salida fijada por esta spec. Un recuento distinto de 0 hallazgos abiertos impide la publicación.
- **Decisión:** parche a `RF-015`, `RNF-009`, `CB-012` y `CA-016`, y ajuste de `CA-017` y del apartado de actores a la misma condición.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-019

- **Descripción:** el inventario conserva el identificador `AUD-NNN` de cada hallazgo y el informe previo al release v0.7.2 registró sus juicios sin número reservado, con `H-01` a `H-03`, y sus observaciones como `OBS-001` a `OBS-004`. El criterio que separa hallazgo de observación no fijaba los identificadores ni el efecto de la observación sobre el recuento.
- **Pregunta:** ¿Con qué identificadores se nombran los hallazgos y las observaciones, y cuál computa en el recuento?
- **Respuesta:** los hallazgos usan el identificador `AUD-NNN` del inventario y conservan su número sin reutilización. Las observaciones usan el identificador `OBS-NNN`, constan con su severidad y su tratamiento y no computan como hallazgo abierto: quedan fuera del recuento de hallazgos y su severidad no altera el cálculo salvo por la condición de tratamiento que `RF-013` declara para las severidades `Alta` y `Media`.
- **Decisión:** parche a `CA-013`, con la forma de los 2 identificadores y la exclusión de la observación del recuento.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

### AMB-020

- **Descripción:** la auditoría previa al release v0.7.2 registró el hallazgo `H-02`: el rol `reviewer` escribió las notas append-only de los reportes de `SPEC-013` y de `SPEC-015`, que son specs publicadas, mientras `§12` del protocolo le concede escritura solo sobre el reporte de la spec en curso. La delegación constaba en `spec.md` y no en la matriz de permisos, y `§12` declara que un permiso no se extiende por analogía.
- **Pregunta:** ¿Qué rol escribe las notas de los reportes de specs publicadas y qué límite rige para el `reviewer`?
- **Respuesta:** las notas append-only de los reportes de specs publicadas las escribe el `documenter` y las firma el propietario en 1 commit firmado con una clave de `docs/sdd/firmantes_autorizados`. El `reviewer` solo escribe el reporte de validación de la spec en curso: no escribe reportes de specs publicadas ni de specs ajenas. El límite se declara en `§12` del protocolo y en la configuración del rol, y el apartado de actores de esta spec deja de atribuirle la nota de un reporte publicado.
- **Decisión:** requisito nuevo `RF-016`, criterio `CA-018` y parche al apartado de actores y permisos.
- **Fecha:** 2026-11-21 (UTC).
- **Responsable:** Agent Sebaxtian.

## Casos borde nuevos

La ampliación añade 6 casos borde:

- `CB-008`: un estado nuevo sobre un hallazgo que ya figura en el inventario conserva el identificador y registra el informe que lo declara — `AMB-011`.
- `CB-009`: un juicio sin regla normativa citada se registra como observación y no computa como hallazgo abierto — `AMB-012`.
- `CB-010`: un veredicto que contradice el recuento del inventario se registra con la fila que sostiene la diferencia — `AMB-013`.
- `CB-011`: una violación histórica sin cierre por artefacto exige ratificación firmada, con efecto retroactivo limitado al régimen y sin reescritura del contenido publicado — `AMB-014`.
- `CB-012`: un veredicto distinto de `CONFORME` impide el release v0.7.2 y conserva la spec en `validated` — `AMB-015`.
- `CB-013`: un informe de auditoría sin fila en el inventario de hallazgos deja la verificación en rojo y detiene la integración — `AMB-011`.

`AMB-018` sustituye en `CB-012` el valor del veredicto por el recuento de hallazgos abiertos: el caso conserva su número y su efecto sobre la publicación del release v0.7.2.

Los 7 casos borde de la versión 0.1.0 se conservan con la redacción que `AMB-001`, `AMB-003`, `AMB-004`, `AMB-005`, `AMB-006`, `AMB-007`, `AMB-008` y `AMB-009` fijan.

## Parches aplicados a `spec.md`

- [x] `RF-001` con la prohibición de fijar el veredicto, el recuento de hallazgos y el conjunto de dimensiones de un informe posterior, la remisión a §16 del protocolo y a la plantilla de `spec.md`, y la forma admitida del criterio — afecta a `RF-001`, `CB-006` y `CA-001`.
- [x] `RF-002` con la regularización por nota append-only y por incremento PATCH de las 2 specs publicadas, la tabla de versión de origen y resultante, y la conservación del texto publicado — afecta a `RF-002` y `CA-002`.
- [x] `RF-003` con la tabla de los 6 artefactos de empaquetado, el orden de corrección entre rangos y la exigencia de spec previa o fix previo — afecta a `RF-003`, `CB-003` y `CA-003`.
- [x] `RF-004` con la ratificación firmada, el cierre del caso `564bac4` con sus 3 rutas, el efecto declarativo y la transcripción del estado de firma — afecta a `RF-004`, `CB-002` y `CA-004`.
- [x] `RF-005` con el registro append-only del resultado de G5 y de G6 y del objeto del tag `v0.7.1` en los 2 soportes, sin alterar matriz, dictamen ni línea de aprobación — afecta a `RF-005`, `CB-005` y `CA-005`.
- [x] `RF-006` con la corrección de las 2 filas T7 al commit de merge publicado, la conservación del destino y del identificador del release y el rechazo de una corrección que los altere — afecta a `RF-006`, `CB-004` y `CA-006`.
- [x] `RF-007` con el cauce del `documenter` para la fila de inventario, la atribución de la fila 34 y el efecto de un informe integrado sin fila — afecta a `RF-007`, `CB-007` y `CA-007`.
- [x] `RF-008` con el cierre de `AUD-106` y de `AUD-107` por evidencia transcrita y la prohibición de declarar cerrada una observación sin artefacto — afecta a `RF-008`, `CB-001` y `CA-008`.
- [x] `RF-009` con la tabla de cierre de 1 fila por observación, el estado cerrado por artefacto presente y la independencia del cierre respecto de un informe posterior — afecta a `RF-009`, `CB-001` y `CA-009`.
- [x] `RF-010` con la regularización de la comprobación del historial de releases, la fila en el registro de cambios bajo `Unreleased` y la prohibición de declarar conforme una regla más estrecha — afecta a `RF-010` y `CA-010`.
- [x] `RF-011` con el inventario único de hallazgos, los 8 campos por fila, el vocabulario cerrado de 5 estados, la conservación del identificador y la prohibición de integrar un informe o un hallazgo sin fila — afecta a `RF-011`, `CB-008`, `CB-013` y `CA-012`.
- [x] `RF-012` con la exigencia de citar la regla normativa con ruta, capítulo y línea, la figura de la observación, su exclusión del recuento y su efecto acotado sobre el veredicto — afecta a `RF-012`, `CB-009` y `CA-013`.
- [x] `RF-013` con la tabla de 4 condiciones del veredicto, la precedencia de los 4 valores, la definición de `CONFORME` y el rechazo de un veredicto que contradiga el recuento — afecta a `RF-013`, `CB-010` y `CA-014`.
- [x] `RF-014` con la ratificación firmada de las violaciones históricas, los 7 casos, el efecto retroactivo limitado al régimen y la prohibición de reescribir el contenido publicado — afecta a `RF-014`, `CB-011` y `CA-015`.
- [x] `RF-015` con la auditoría sobre el estado integrado, el veredicto `CONFORME` como condición del release v0.7.2, la transcripción del informe y la secuencia G5, auditoría y G6 — afecta a `RF-015`, `CB-012` y `CA-016`.
- [x] `RNF-005` a `RNF-009` con 1 criterio de verificación por requisito nuevo: campos y filas del inventario, regla citada, coincidencia del veredicto con el recuento, ratificación firmada y release con auditoría previa — afecta a `RNF-005`, `RNF-006`, `RNF-007`, `RNF-008`, `RNF-009` y `CA-017`.
- [x] `RNF-001` a `RNF-004` con el recuento nulo de autorreferencia, la conservación de requisitos publicados, el límite de 300 segundos de la validación agregada y la firma de cada modificación publicada — afecta a `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004` y `CA-011`.
- [x] `## Actores y permisos` con la ratificación firmada del propietario, la escritura del `documenter` sobre la fila de inventario del corpus y sobre la fila del inventario de hallazgos, las 3 correcciones de rango 3 y de rango 5, la competencia del `coder` sobre las comprobaciones del historial de releases y del cálculo del veredicto, el límite de escritura del rol de auditoría y el cálculo del veredicto desde el inventario — afecta a `RF-001`, `RF-004`, `RF-007`, `RF-010`, `RF-011` y `RF-013`.
- [x] `## Fuera de alcance` con la prohibición de reescribir historia publicada, de mover o recrear los 2 tags, de ampliar las ventanas de legado, de declarar compuertas o un veredicto de conformidad, de publicar el release v0.7.2, de modificar los informes publicados y de reasignar o reabrir un identificador — afecta a `RF-002`, `RF-004`, `RF-005`, `RF-009`, `RF-011` y `RF-015`.
- [x] `## Trazabilidad con el informe de auditoría` con las 11 observaciones del informe de v0.7.1, su severidad, su requisito y su criterio, y `### Trazabilidad de los dieciséis hallazgos del inventario` con 1 fila por hallazgo, las 5 exenciones incluidas — afecta a `RF-001` a `RF-015` y a `CA-001` a `CA-017`.
- [x] Frontmatter con `version` 0.3.0, `updated` 2026-11-21 y `status` `clarified`; fila nueva en `## Historial de cambios` y conservación de la fila T1 en `### Historial de transiciones`, sin transición nueva porque el estado no cambia — afecta a la estructura de `spec.md`.
- [x] `RF-011` con el alcance a los informes de auditoría presentes en `docs/sdd/`, sin límite de 5 ni enumeración cerrada, y con la fila del inventario exigida en cada informe integrado — afecta a `RF-011`, `RNF-005` y `CA-012`.
- [x] `RF-015`, `RNF-009` y `CB-012` con la condición de 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento, sin nombrar los valores del veredicto, y con el recuento de hallazgos abiertos transcrito en la entrada del release — afecta a `RF-015`, `RNF-009`, `CB-012`, `CA-016` y `CA-017`.
- [x] `CA-016` con la condición expresada sobre el inventario, la transcripción del identificador del informe y del recuento de hallazgos abiertos, la precedencia de G5 sobre G6 y el efecto de un recuento distinto de 0 — afecta a `CA-016`.
- [x] `CA-013` con el identificador `AUD-NNN` del hallazgo, el identificador `OBS-NNN` de la observación y la exclusión de la observación del recuento de hallazgos — afecta a `CA-013`.
- [x] `RF-016` con la autoría del `documenter` y la firma del propietario sobre la nota append-only de un reporte publicado, el límite de escritura del `reviewer` al reporte de la spec en curso y la declaración de ese límite en `§12` y en la configuración del rol — afecta a `RF-016` y `CA-018`.
- [x] `RF-017` con la actualización de `MEMORY.md` al mismo estado y al mismo release pendiente que el frontmatter y que la fila del índice, la cita del índice como fuente y la fila de corrección en el historial de cambios — afecta a `RF-017` y `CA-019`.
- [x] `CA-018` y `CA-019` al final de `## Criterios de aceptación`, con la numeración existente conservada y los 2 identificadores nuevos en el orden de lectura — afecta a `CA-018` y `CA-019`.
- [x] `## Actores y permisos` con el límite del `reviewer` al reporte de la spec en curso y con la nota append-only de un reporte publicado a cargo del `documenter` y firmada por el propietario — afecta a `RF-007`, `RF-016` y `CA-018`.
- [x] Frontmatter con `status` `implementing`, `version` 0.9.0 y `updated` 2026-11-21; fila 0.9.0 en `## Historial de cambios`; fila T9 en `### Historial de transiciones`; nota de zona UTC de las fechas documentales; retiro de la mención de la integración en la fila T6 — afecta a la estructura de `spec.md` y a `OBS-003` y `OBS-004`.

## Decisiones de negocio

- El objeto auditado no determina la auditoría. Un requisito de una spec no puede fijar el veredicto, el recuento de hallazgos ni el conjunto de dimensiones del informe que evalúa esa misma spec, porque la compuerta que se apoya en ese informe perdería evidencia independiente. El criterio solo puede exigir el artefacto y su evidencia.
- La corrección de lo publicado es declarativa y firmada: se conserva el contenido, se registra el acto del propietario y no se reescribe el historial. La ratificación sustituye a la reversión y la nota append-only sustituye a la reescritura.
- El alcance de la rama de empaquetado es una lista cerrada de 6 artefactos y no una recomendación; el rango 3 fija el conjunto y el rango 4 lo replica, en el orden de precedencia de la constitución.
- La autoría de la fila de inventario corresponde al `documenter` y no al rol de auditoría: el auditor acredita hechos y no mantiene el índice del corpus.
- El cierre de una observación se acredita con su artefacto y su evidencia, no con el informe de una auditoría posterior. Una observación sin artefacto permanece vigente y se registra como tal.
- Esta spec no emite veredicto de conformidad del régimen. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen, y no sustituye la firma del propietario en G1, G4 ni G6.
- El veredicto deja de depender del criterio de cada pasada: se calcula desde el estado de las filas del inventario y su valor `CONFORME` exige 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. Un juicio sin regla normativa citada es observación y no hallazgo, porque un hallazgo sin norma identificada no se puede verificar ni cerrar con artefacto.
- El inventario es la memoria del régimen y no un informe: conserva el identificador emitido, admite estados sucesivos sobre la misma fila y no renumera. Su escritura corresponde al `documenter` y no al rol de auditoría, que acredita hechos y no mantiene el registro.
- Las violaciones históricas que ningún artefacto repara se cierran por ratificación firmada del propietario, con efecto retroactivo limitado al régimen. La ratificación no reescribe el contenido publicado ni el informe de origen: acredita la autoría y declara el efecto, con la misma lógica declarativa de la ratificación del commit `564bac4`.
- El release v0.7.2 se publica solo sobre una auditoría del estado integrado con 0 hallazgos abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento. Auditar el estado integrado y no el estado de la rama de trabajo evita que el informe califique un árbol distinto del que se publica, y la condición se expresa sobre el inventario y no sobre el valor del veredicto, que emite el rol de auditoría.
- El objeto auditado no determina la auditoría: la condición de publicación cuenta hallazgos abiertos y observaciones sin tratamiento, y no nombra el veredicto. Nombrar el valor del veredicto en el contrato restablece la autorreferencia que `RF-001` prohíbe y anula la independencia de la evidencia.
- El inventario alcanza cada informe de auditoría presente en `docs/sdd/`: el alcance lo fija la ubicación del archivo y no la fecha de corte con la que se redactó el inventario, de modo que un informe nuevo computa en el cálculo desde su integración.
- El hallazgo conserva el identificador `AUD-NNN` y la observación usa `OBS-NNN`. La observación documenta un juicio sin regla normativa citada y no computa en el recuento de hallazgos.
- La nota append-only de un reporte publicado la escribe el `documenter` y la firma el propietario; el `reviewer` solo redacta el reporte de su propia spec. La delegación escrita no amplía una matriz de permisos que `§12` declara cerrada.
- La reapertura corrige las cuatro observaciones del informe previo: `OBS-003` y `OBS-004` en `spec.md`, y `OBS-001` y `OBS-002` en `docs/sdd/inventario_hallazgos.md` y en `docs/Flujo_de_Trabajo_Git.md`, que escribe el `documenter` en la etapa Implement de esta reapertura.
