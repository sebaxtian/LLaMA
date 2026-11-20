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

## Casos borde nuevos

Sin casos borde nuevos en esta clarificación: los 7 casos borde de `spec.md` se redactaron en la versión 0.1.0 y esta clarificación ajusta su redacción en los puntos que `AMB-001`, `AMB-003`, `AMB-004`, `AMB-005`, `AMB-006`, `AMB-007`, `AMB-008` y `AMB-009` fijan.

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
- [x] `RNF-001` a `RNF-004` con el recuento nulo de autorreferencia, la conservación de requisitos publicados, el límite de 300 segundos de la validación agregada y la firma de cada modificación publicada — afecta a `RNF-001`, `RNF-002`, `RNF-003`, `RNF-004` y `CA-011`.
- [x] `## Actores y permisos` con la ratificación firmada del propietario, la escritura del `documenter` sobre la fila de inventario y las 3 correcciones de rango 3 y de rango 5, la competencia del `coder` sobre la comprobación del historial de releases y el límite de escritura del rol de auditoría — afecta a `RF-001`, `RF-004`, `RF-007` y `RF-010`.
- [x] `## Fuera de alcance` con la prohibición de reescribir historia publicada, de mover o recrear los 2 tags, de ampliar las ventanas de legado y de declarar compuertas o un veredicto de conformidad — afecta a `RF-002`, `RF-004`, `RF-005` y `RF-009`.
- [x] `## Trazabilidad con el informe de auditoría` con las 11 observaciones, su severidad, su requisito y su criterio, incluido el doble destino de `AUD-088` y de `AUD-109` — afecta a `RF-001` a `RF-010` y a `CA-001` a `CA-011`.
- [x] Frontmatter con `version` 0.2.0, `updated` 2026-11-21 y `status` `clarified`; fila nueva en `## Historial de cambios` y fila T1 en `### Historial de transiciones` — afecta a la estructura de `spec.md`.

## Decisiones de negocio

- El objeto auditado no determina la auditoría. Un requisito de una spec no puede fijar el veredicto, el recuento de hallazgos ni el conjunto de dimensiones del informe que evalúa esa misma spec, porque la compuerta que se apoya en ese informe perdería evidencia independiente. El criterio solo puede exigir el artefacto y su evidencia.
- La corrección de lo publicado es declarativa y firmada: se conserva el contenido, se registra el acto del propietario y no se reescribe el historial. La ratificación sustituye a la reversión y la nota append-only sustituye a la reescritura.
- El alcance de la rama de empaquetado es una lista cerrada de 6 artefactos y no una recomendación; el rango 3 fija el conjunto y el rango 4 lo replica, en el orden de precedencia de la constitución.
- La autoría de la fila de inventario corresponde al `documenter` y no al rol de auditoría: el auditor acredita hechos y no mantiene el índice del corpus.
- El cierre de una observación se acredita con su artefacto y su evidencia, no con el informe de una auditoría posterior. Una observación sin artefacto permanece vigente y se registra como tal.
- Esta spec no emite veredicto de conformidad del régimen. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen, y no sustituye la firma del propietario en G1, G4 ni G6.
