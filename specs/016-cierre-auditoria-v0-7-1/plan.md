# Plan técnico — SPEC-016

*Artefacto de rango 6: diseño del cierre de la auditoría de `v0.7.1`, con las decisiones `DEC-001` a `DEC-008`, los contratos `C-1` a `C-9`, la estrategia de testing y la matriz de cobertura de los 15 requisitos funcionales, los 9 requisitos no funcionales y los 13 casos borde.*

## Referencias

- `spec.md`: `SPEC-016`, versión 0.3.0, estado `clarified`, con 15 requisitos funcionales, 9 requisitos no funcionales, 13 casos borde y 17 criterios de aceptación; G1 firmada por `Agent Sebaxtian` (2026-11-21).
- `clarify.md`: `SPEC-016`, cerrado con `AMB-001` a `AMB-016` resueltos, 21 parches aplicados a `spec.md` y las 10 decisiones de negocio que fijan el alcance del cierre.
- `docs/sdd/auditoria_final_v0_7_1.md`: veredicto global `NO CONFORME` sobre el commit `5ba048d`, con 11 hallazgos vigentes y la tabla de los diez identificadores del corte anterior.
- `docs/sdd/auditoria_cumplimiento_sdd.md`: informe de origen con 41 hallazgos, `AUD-001` a `AUD-094`, y la hoja de ruta B1 a B4.
- `docs/sdd/auditoria_cierre_v0_7_0.md`: reauditoría de cierre con 16 hallazgos nuevos, `AUD-008` a `AUD-097`, y las 5 exenciones `AUD-003`, `AUD-004`, `AUD-005` y `AUD-053`.
- `docs/sdd/auditoria_final_v0_7_0.md`: reauditoría final con 7 hallazgos nuevos, `AUD-038` a `AUD-102`, entre ellos `AUD-075`.
- `docs/sdd/auditoria_posterior_v0_7_0.md`: reauditoría posterior con 10 hallazgos nuevos, `AUD-039` a `AUD-100`, entre ellos `AUD-087`, `AUD-088`, `AUD-089` y `AUD-090`.
- `docs/constitution.md`: tabla de siete rangos y categoría sin rango de §6, registro de aprobaciones de §7, prohibición de reescribir historia y auditoría de conformidad previa al release de §8.
- `AGENTS.md`: cadena `RF/CB → CA → T → evidencia`, seis roles, línea de registro de aprobación y prohibición de declarar compuertas.
- `docs/sdd/PROTOCOLO_OPERATIVO.md`: §5 con la tabla de transiciones, §6 con la tabla de compuertas, §9 con las reglas de versionado, §11 con el registro de aprobación, §12 con la matriz de roles, §13 con la integración y el release, §15 con la rama de release y §16 con el control de cambios y la auditoría.
- `docs/Flujo_de_Trabajo_Git.md`: procedimiento obligatorio de release del paso 1 al paso 8, tabla de compuertas G5 y G6, bloque de check exigible y excepción de ramas de release.
- `docs/sdd/plantillas/spec.md`: sección de aprobaciones, historial de cambios e historial de transiciones, y lista de prohibiciones de la plantilla.
- `docs/sdd/plantillas/informe_auditoria.md`: diez secciones, escalas de veredicto y de severidad, y numeración `AUD-NNN`.
- `docs/sdd/README.md`: tabla de autoridad y tabla de inventario del corpus con 36 filas de datos y la regla de inventario.
- `specs/013-cierre-reauditoria-conformidad/spec.md` y `specs/015-cierre-auditoria-posterior/spec.md`: requisitos y criterios publicados que fijan el veredicto y el recuento de un informe posterior.
- `specs/014-cierre-observaciones-finales/spec.md` y `specs/015-cierre-auditoria-posterior/spec.md`: filas T7 que nombran el commit de empaquetado como destino del tag, versiones 0.8.1 y 0.8.0.
- `specs/015-cierre-auditoria-posterior/validation_report.md`: nota de la línea 77 que anuncia una transcripción del objeto del tag inexistente en el documento publicado.
- `CHANGELOG.md`: entrada `v0.7.1` de las líneas 13 a 29 sin el resultado de G5 ni el de G6, y `Unreleased` vacía de la línea 11.
- `tools/sdd/validate.py`: `C-02` y `C-10` para el release, `C-14` para el enlace `CA → T`, `C-18` para la regularización y el registro de comprobaciones de §14 del protocolo.
- `tools/sdd/tests/test_agent_permissions.py`: `problemas_de_inventario` en la línea 1977 y `test_historial_de_releases` en la línea 1991.
- `.opencode/agents/auditor.md`: frontmatter de permisos con `docs/sdd/auditoria_*.md` como única concesión de escritura.

## Naturaleza del entregable

La spec produce una combinación declarada de normativa, registro documental, acto firmado, registro de spec y pruebas:

- Norma de rango 3: `docs/sdd/PROTOCOLO_OPERATIVO.md`, con la prohibición de autorreferencia de §16, la regla de hallazgo con regla citada, el cálculo del veredicto, el cauce de la fila de inventario de §12 y el conjunto de 6 artefactos de empaquetado de §15.
- Norma de rango 4: `docs/Flujo_de_Trabajo_Git.md`, con el mismo conjunto de 6 artefactos en el paso 3, la auditoría previa al release y el destino del tag en la evidencia de la fila T7.
- Norma de rango 5: `docs/sdd/plantillas/spec.md`, con la prohibición de fijar el veredicto de una auditoría futura, y `docs/sdd/plantillas/informe_auditoria.md`, con el campo de regla citada, la figura de la observación y el cálculo del veredicto.
- Registro sin rango: `docs/sdd/inventario_hallazgos.md` con 1 fila por identificador `AUD-NNN` de los 5 informes, y `docs/sdd/ratificacion_historica.md` con el acto firmado del propietario.
- Registro de spec de rango 6: las 2 notas append-only de autorreferencia, la nota del resultado de G5 y de G6 de `SPEC-015`, las 2 filas T7 corregidas y las filas de motivo de las 3 specs regularizadas.
- Registro de cambios de raíz: `CHANGELOG.md`, con las filas de `Unreleased`, el bloque de registro de la entrada `v0.7.1` y la declaración del commit ratificado.
- Pruebas de rango 7: las comprobaciones de `tools/sdd/tests/` sobre regla citada, cálculo del veredicto, compleción del inventario, destino del tag, alcance de 6 artefactos, autorreferencia y cierre de los 16 hallazgos, con pareja positiva y negativa.

No produce scripts `.bat`, no modifica `src/`, `models/`, `bin/`, `llama.cpp/` ni `.github/`, no reescribe el contenido publicado que la ratificación declara, no mueve ni recrea los tags `v0.7.0` y `v0.7.1`, no modifica los 5 informes de auditoría y no declara compuerta alguna. Un resultado favorable del validador acredita estructura, coherencia interna y trazabilidad declarada, no la conformidad del régimen.

## Arquitectura

### Componentes, responsabilidad y límite

| Componente | Artefacto | Responsabilidad | Límite | Rol que escribe |
|---|---|---|---|---|
| Inventario de hallazgos | `docs/sdd/inventario_hallazgos.md` | Conserva 1 fila por identificador `AUD-NNN` de los 5 informes con los 8 campos de `RF-011`, el estado vigente y la evidencia de cierre por ruta y línea | No renumera ni reutiliza un identificador; no declara veredicto; no reescribe el informe de origen | `documenter` |
| Anexo de observaciones | `docs/sdd/inventario_hallazgos.md`, sección «Observaciones y tratamientos» | Registra el juicio sin regla citada, su severidad y la decisión del propietario que lo trata | No computa como hallazgo abierto ni recibe identificador `AUD-NNN` nuevo | `documenter` |
| Acta de ratificación | `docs/sdd/ratificacion_historica.md` | Declara el alcance, la fecha, las rutas y los identificadores afectados y el efecto retroactivo limitado al régimen | No reescribe el contenido publicado ni el informe de origen; no alcanza regla ajena al régimen | propietario |
| Prohibición de autorreferencia | `docs/sdd/PROTOCOLO_OPERATIVO.md` §16 y `docs/sdd/plantillas/spec.md` | Declara que una spec no fija el veredicto, el recuento ni el conjunto de dimensiones de un informe posterior | No prohíbe citar un informe como evidencia ni exigir su existencia y su transcripción | `documenter` |
| Regla de hallazgo y veredicto | `docs/sdd/PROTOCOLO_OPERATIVO.md` §16 y `docs/sdd/plantillas/informe_auditoria.md` | Exige la regla citada por ruta, capítulo y línea, separa la observación del hallazgo y fija la tabla de cálculo con su precedencia | No emite veredicto; no sustituye al rol de auditoría | `documenter` |
| Cauce de la fila de inventario | `docs/sdd/PROTOCOLO_OPERATIVO.md` §12, la plantilla del informe y `.opencode/agents/auditor.md` | Declara que la fila la escribe el `documenter` antes de integrar el informe y limita la escritura del rol de auditoría a su informe | No atribuye la fila al rol de auditoría; no amplía su permiso | `documenter` y propietario sobre `.opencode/agents/auditor.md` |
| Conjunto de empaquetado | `docs/sdd/PROTOCOLO_OPERATIVO.md` §15 y `docs/Flujo_de_Trabajo_Git.md` paso 3 y excepción | Declara los 6 artefactos con su modificación admitida, el orden de corrección del rango 3 antes que el rango 4 y la exigencia de spec previa o fix previo | No admite una séptima ruta en la rama `release/vX-Y-Z`; no introduce código ni configuración | `documenter` |
| Auditoría previa al release | `docs/Flujo_de_Trabajo_Git.md`, sección de validaciones de release | Fija la secuencia G5, auditoría sobre el estado integrado en `dev` y G6, y el efecto de un veredicto distinto de `CONFORME` | No publica el release; no declara G6 | `documenter` |
| Registro del release `v0.7.1` | `specs/015-cierre-auditoria-posterior/validation_report.md` y la entrada `v0.7.1` de `CHANGELOG.md` | Transcribe el resultado de G5 y de G6 y el objeto anotado del tag, con su mensaje y su commit objetivo | Append-only: no altera la matriz, el dictamen ni la línea de aprobación | `reviewer` para la nota y `documenter` para la entrada |
| Regularización de specs publicadas | `specs/013-cierre-reauditoria-conformidad/`, `specs/014-cierre-observaciones-finales/` y `specs/015-cierre-auditoria-posterior/` | Añade las 2 notas de autorreferencia, corrige las 2 filas T7 e incrementa 1 incremento PATCH por corrección con su fila de motivo | No renumera la spec; no altera `status`, el campo `release` ni el destino `released` | `reviewer` para las notas y `planner` para las filas T7 |
| Comprobaciones del mecanismo | `tools/sdd/hallazgos.py`, `tools/sdd/validate.py` y `tools/sdd/tests/test_hallazgos.py` | Calcula el veredicto desde el inventario, controla la compleción, exige la regla citada, compara los 6 artefactos, verifica el destino del tag y detecta la autorreferencia | Solo lee texto del repositorio; no escribe artefactos, no consulta el remoto y no crea tags | `coder` |
| Contrato de la feature | `specs/016-cierre-auditoria-v0-7-1/` | Declara requisitos, decisiones, tareas y evidencia | No reabre el contenido funcional de `SPEC-013`, `SPEC-014` ni `SPEC-015` | `planner` |

### Orden de las correcciones

El orden evita que una comprobación nueva declare en rojo un artefacto todavía sin corregir y deja la ratificación después de los artefactos que la sostienen:

1. Pruebas y funciones puras de `tools/sdd/` en rojo y después en verde, porque fijan el contrato verificable del inventario y del veredicto.
2. Norma de rango 3 y norma de rango 4, porque el rango 3 fija el conjunto de empaquetado y el rango 4 lo replica en el orden de precedencia de la constitución.
3. Plantillas de rango 5, porque fijan la forma que el inventario y los informes posteriores deben cumplir.
4. Inventario de hallazgos, porque sus filas citan los artefactos de los pasos 2 y 3 y la evidencia por ruta y línea.
5. Acta de ratificación del propietario, porque cierra las 5 exenciones y las 2 modificaciones sin firma y habilita el estado `cerrado por ratificación` de 5 filas.
6. Registro del corpus, registro de cambios, notas append-only y filas T7, porque describen los artefactos anteriores.
7. Verificación agregada, que contrasta los recuentos de `RNF-001` a `RNF-009` sobre el commit validado.

### Flujo de cálculo del veredicto

1. El informe de auditoría emite hallazgos con regla citada y observaciones sin regla citada.
2. El `documenter` escribe la fila de cada hallazgo en `docs/sdd/inventario_hallazgos.md` antes de integrar el informe.
3. La función `veredicto()` clasifica cada fila por su estado y aplica la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME`.
4. La comprobación contrasta el veredicto declarado en el informe con el calculado desde las filas y registra el error con la fila que sostiene la diferencia.
5. El rol de auditoría declara el veredicto; la comprobación no lo declara y no lo sustituye.

## Contratos

### C-1 Fila del inventario

Cada fila de la tabla de hallazgos declara los 8 campos de `RF-011` en este orden: `Identificador`, `Dimensión`, `Severidad`, `Informe de origen`, `Regla normativa citada`, `Estado`, `Evidencia de cierre` e `Informe que declara el estado`. El identificador conserva la forma `AUD-NNN` y no se repite. La dimensión usa `D1` a `D11`. La severidad usa `Crítica`, `Alta`, `Media` o `Baja`.

### C-2 Vocabulario cerrado del estado

El campo `Estado` admite 5 valores y ningún otro: `cerrado`, `parcial`, `vigente`, `cerrado por exención` y `cerrado por ratificación`. Son estados cerrados `cerrado` y `cerrado por ratificación`; son estados abiertos `parcial`, `vigente` y `cerrado por exención`. Una fila con un valor fuera del conjunto produce error con el identificador.

### C-3 Cita normativa

El campo `Regla normativa citada` usa la forma `ruta §capítulo:línea`, con la ruta relativa terminada en `.md`, el capítulo entre `1` y `16` y la línea en dígitos. Ejemplo de forma: `docs/constitution.md §7:76`. Una fila sin esa forma produce error con el identificador y deja el veredicto susceptible de `NO VERIFICABLE`.

### C-4 Cálculo del veredicto

La función pura `veredicto(filas)` recibe las filas del inventario y devuelve 1 de los 4 valores de la tabla de `RF-013`. La precedencia se evalúa en este orden y el primer valor que se cumple es el resultado: `NO CONFORME` con 1 o más abiertos de severidad `Crítica` o `Alta`; `NO VERIFICABLE` con 0 de esas severidades y 1 o más filas sin regla citada o sin evidencia de cierre; `PARCIAL` con 0 filas sin regla o sin evidencia y 1 o más abiertos de severidad `Media` o `Baja`, o 1 o más observaciones de severidad `Alta` o `Media` sin tratamiento; `CONFORME` con 0 abiertos y 0 observaciones de severidad `Alta` o `Media` sin tratamiento.

### C-5 Extracción y compleción

La función `identificadores_de_informes()` lee los 5 informes declarados en la tabla de origen, extrae cada token con la forma `AUD-NNN`, descarta duplicados y ordena de forma ascendente. El conjunto resultante del corte es de 82 identificadores. La comprobación compara ese conjunto con el de las filas del inventario y produce 1 error por identificador sin fila y 1 error por fila sin informe de origen, con la ruta del archivo y el identificador.

### C-6 Conjunto canónico de empaquetado

Los 6 artefactos se codifican con las claves `A1` a `A6` de la tabla de `RF-003`, cada una con su modificación admitida. La comprobación extrae del rango 3 y del rango 4 las claves declaradas y compara los 2 conjuntos; una diferencia produce un error que nombra la clave y el rango, y no declara alineada la enumeración.

### C-7 Destino del tag

La evidencia de la fila T7 declara el identificador del commit de merge publicado en `main`, la palabra `merge` y la relación de ancestría con el commit de empaquetado. La comprobación exige 1 identificador hexadecimal de 7 a 40 caracteres, el token `main` y la declaración de ancestría, y rechaza la frase que declara el commit de empaquetado como destino del tag. La comprobación no altera el destino `released`, el campo `release` ni el identificador del release.

### C-8 Nota append-only

La nota se añade al final de la sección que la recibe, con el identificador del requisito que la habilita, el contenido exigido y la fecha UTC. La nota no retira línea alguna del documento y no modifica la matriz ni el dictamen. La comprobación cuenta las líneas retiradas del rango publicado y exige 0.

### C-9 Acta de ratificación

El acta declara la fecha UTC, el alcance con los 5 identificadores de exención y los 2 identificadores de commit, las rutas afectadas, el efecto retroactivo limitado al régimen y la referencia a la lista de `docs/sdd/firmantes_autorizados`. La comprobación exige que el commit que introduce el acta tenga firma verificable y que su clave figure en la lista; una firma ausente o no verificable deja la ratificación sin efecto.

## Decisiones técnicas

### DEC-001

- **Decisión:** el inventario se deriva de forma mecánica de los 5 informes de `docs/sdd/`: se extrae cada token `AUD-\d{3}`, se descarta el duplicado y se escribe 1 fila por identificador en orden ascendente. El estado de la fila es el que declara el informe más reciente en el orden de corte `auditoria_cumplimiento_sdd.md`, `auditoria_cierre_v0_7_0.md`, `auditoria_final_v0_7_0.md`, `auditoria_posterior_v0_7_0.md` y `auditoria_final_v0_7_1.md`, y el campo de informe que declara el estado transcribe ese informe con su fecha de corte. La compleción se controla con la comparación de conjuntos y con el recuento de 82 filas para 82 identificadores.
- **Justificación:** la derivación mecánica hace que 2 redactores independientes obtengan el mismo conjunto y convierte la omisión en un error con nombre y ruta, no en una apreciación del redactor. El orden de corte elimina la ambigüedad entre estados sucesivos sobre el mismo identificador y satisface `CB-008`.
- **Alternativas descartadas:** 1 inventario por informe, que duplicaría 82 identificadores en 5 tablas y rompería la conservación del identificador; el inventario reducido a los 16 hallazgos del cierre, que perdería la memoria de los 66 cerrados y haría irrepetible el cálculo del veredicto; la lista escrita a mano sin extracción, que no detecta la omisión.

### DEC-002

- **Decisión:** un hallazgo es el juicio que cita la regla normativa incumplida con ruta, capítulo y línea; un juicio sin esa cita se registra como observación en el anexo de observaciones y tratamientos y queda fuera del recuento de hallazgos. La severidad de la observación `Alta` o `Media` impide `CONFORME` mientras carezca de tratamiento, y la de severidad `Baja` no lo impide. Un tratamiento es la decisión del propietario con fecha e identificador de commit que declara el efecto y el destino de la observación.
- **Justificación:** un hallazgo sin norma identificada no se puede verificar ni cerrar con artefacto, de modo que su cómputo como abierto haría imposible el veredicto `CONFORME` por causas no reparables. La figura de la observación conserva el juicio sin darle el efecto de un hallazgo y satisface `CB-009`.
- **Alternativas descartadas:** computar como hallazgo cada juicio de forma, de redacción o de autoría, que es el defecto que `AUD-109` registra; aceptar la cita por sección sin línea, que no permite contrastar la regla con la práctica observada; eliminar el juicio sin regla, que perdería la observación sin dejar registro.

### DEC-003

- **Decisión:** el veredicto se calcula con la función pura `veredicto(filas)` desde el estado de las filas del inventario y el estado de las observaciones, con la precedencia `NO CONFORME`, `NO VERIFICABLE`, `PARCIAL` y `CONFORME` de `C-4`. La comprobación contrasta el veredicto declarado por el informe con el calculado y produce un error con la fila que sostiene la diferencia. La autorreferencia se detecta por la concurrencia de una referencia a un informe concreto —ruta `docs/sdd/auditoria_*.md`, `auditoría de cierre` o `informe de auditoría de vX.Y.Z`— y una salida fijada —token `CONFORME`, `NO CONFORME`, `PARCIAL` o `NO VERIFICABLE`, o un recuento con la forma `N de M`—; una spec publicada con esa forma solo pasa si su reporte porta la nota de autorreferencia de `RF-002`.
- **Justificación:** el cálculo desde el inventario elimina la dependencia del criterio de cada pasada y hace reproducible el veredicto. La detección por referencia concreta más salida fijada distingue la prohibición de la cita de evidencia y no marca los requisitos que definen el cálculo, como `RF-013` de esta spec.
- **Alternativas descartadas:** derivar el veredicto del promedio de los veredictos por dimensión, que es la regla que `AUD-109` declara insostenible; prohibir la palabra `veredicto` en una spec, que marcaría la definición del propio cálculo; confiar el contraste al rol de auditoría, que dejaría el cálculo sin comprobación independiente.

### DEC-004

- **Decisión:** las violaciones históricas se cierran con 1 acta firmada del propietario en `docs/sdd/ratificacion_historica.md`, introducida en 1 commit firmado con una clave de `docs/sdd/firmantes_autorizados`. El alcance son las 5 exenciones `AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053` y las 2 modificaciones sin firma de los commits `494db2e` y `564bac4`, con la ruta de cada artefacto publicado. El efecto retroactivo se limita al régimen: la autoría queda acreditada por la firma del acta, el contenido publicado conserva su texto y ninguna regla ajena al régimen queda alcanzada. La fila del inventario pasa a `cerrado por ratificación` con el identificador del commit del acta.
- **Justificación:** ninguna de las 7 causas admite un artefacto que la repare sin reescribir contenido publicado o historia integrada, y la constitución prohíbe ambas. El acta firmada acredita la autoría y declara el efecto sin reescribir, y conserva la trazabilidad del identificador en la fila del inventario.
- **Alternativas descartadas:** revertir el contenido publicado, que la constitución prohíbe; reescribir el historial con rebase o copia manual, que también prohíbe; mantener las 5 exenciones como estado abierto, que impediría `CONFORME` y dejaría el cierre sin instrumento.

### DEC-005

- **Decisión:** el conjunto de la rama `release/vX-Y-Z` es una lista cerrada de 6 artefactos con las claves `A1` a `A6` de `RF-003`, declarada primero en §15 del rango 3 y replicada después en el paso 3 del rango 4, con el mismo límite en los 2 documentos. Cualquier ruta distinta exige una spec previa o un fix previo. El tag anotado apunta al commit de merge publicado en `main`, y la evidencia de la fila T7 declara ese identificador y su relación de ancestría con el commit de empaquetado.
- **Justificación:** el empaquetado escribe filas de historial de cambios y de transiciones que la enumeración de 4 artefactos no admitía, de modo que la lista cerrada debe declarar lo que la práctica exige. El orden del rango 3 antes que el rango 4 respeta la precedencia de la constitución y evita repetir el orden inverso que `AUD-103` registra.
- **Alternativas descartadas:** conservar 4 artefactos y declarar la fila de historial como excepción, que multiplicaría las excepciones ya registradas; declarar una lista abierta con la condición de coherencia, que no permite comparar conjuntos; mantener el commit de empaquetado como destino del tag, que contradice el objeto verificado del tag.

### DEC-006

- **Decisión:** la comprobación del historial de releases admite las filas de historial de cambios y de transición que el empaquetado escribe y la constante de estados que admite `released`, y su regularización consta en 1 fila del registro de cambios bajo `Unreleased`. La auditoría previa al release se ejecuta sobre el estado integrado en `dev` después de G5 y antes de G6, y su veredicto debe ser `CONFORME` para publicar; la entrada del release transcribe el identificador del informe y el veredicto. Un veredicto distinto de `CONFORME` impide la publicación, conserva la spec en `validated` y transcribe el motivo con el hallazgo que lo sostiene.
- **Justificación:** una comprobación más estrecha que el alcance del empaquetado produce rojo sobre un artefacto conforme, y auditar la rama de trabajo calificaría un árbol distinto del que se publica. La secuencia G5, auditoría y G6 hace que la condición de G6 se apoye en evidencia posterior a la integración y anterior a la firma.
- **Alternativas descartadas:** declarar la comprobación conforme sin regularizarla, que es el defecto que el residuo de `AUD-088` registra; auditar la rama de trabajo antes de la integración, que deja el veredicto sobre un árbol no publicado; auditar después de G6, que convierte la condición en un acto posterior al que pretende autorizar.

### DEC-007

- **Decisión:** 11 hallazgos se cierran con el artefacto que los satisface y la evidencia transcrita por ruta y línea en el commit validado, y 5 se cierran por la ratificación de `DEC-004` con el estado `cerrado por ratificación`. La tabla de cierre de `RF-009` registra 1 fila por observación con su artefacto y su evidencia, y el estado cerrado figura solo cuando el artefacto consta en el commit validado. El cierre de `AUD-106` transcribe el listado de ramas locales sin `release/v0-7-0` ni `release/v0-7-1`, y el de `AUD-107` transcribe la fila 35 de la tabla de inventario del corpus y el resultado de la suite.
- **Justificación:** el cierre por artefacto es verificable y no depende de un informe posterior, que evaluaría la spec y no podría ser condición de su propio cierre. La distinción entre artefacto presente y ausente convierte `CB-001` en una regla de estado y no en una apreciación.
- **Alternativas descartadas:** acreditar el cierre con el informe de la auditoría siguiente, que reproduce la autorreferencia de `AUD-109`; declarar cerradas las 16 con la sola mención del requisito, que deja la observación sin evidencia; cerrar las 11 en bloque con 1 fila agregada, que pierde la trazabilidad por identificador.

### DEC-008

- **Decisión:** cada comprobación nueva consta de 1 caso positivo sobre el artefacto del repositorio y 1 caso negativo sobre texto sintético que conserva el defecto, con funciones puras en `tools/sdd/hallazgos.py` que reciben texto y devuelven hallazgos. La integración en `tools/sdd/validate.py` usa esas funciones y añade las comprobaciones al alcance impreso por `--all`. Las pruebas no consultan Git, no acceden a la red y no escriben archivo versionado.
- **Justificación:** la pareja positiva y negativa acredita que la comprobación detecta el defecto y que no lo inventa sobre el artefacto conforme, que es la única forma de que la prueba sobreviva a la corrección. Las funciones puras permiten reproducir el resultado sin depender del estado del repositorio.
- **Alternativas descartadas:** pruebas solo positivas, que pasarían aunque la comprobación no detectara nada; pruebas contra Git real o el remoto, que no son reproducibles y exceden el permiso del rol; pruebas sobre el documento completo sin caso sintético, que no distinguen la detección del cumplimiento.

### DEC-009

- **Decisión:** la reapertura 0.9.0 corrige la condición de publicación sobre el inventario y no sobre el valor del veredicto, amplía el alcance del inventario a cada informe presente en `docs/sdd/`, nombra las observaciones con `OBS-NNN` fuera del recuento y declara la autoría de la nota de un reporte publicado en el `documenter` con firma del propietario. La condición de publicación se verifica con el recuento de hallazgos abiertos y de observaciones de severidad `Alta` o `Media` sin tratamiento.
- **Justificación:** `§16` del protocolo prohíbe que una spec fije el veredicto y el recuento de hallazgos de un informe emitido después de su aprobación. El valor del veredicto es salida del rol de auditoría; el recuento de abiertos es un estado del inventario y se puede contrastar sin anticipar el juicio. La nota de un reporte publicado queda fuera de la matriz de permisos del `reviewer`, que `§12` limita al reporte de la spec en curso.
- **Alternativas descartadas:** conservar el valor `CONFORME` en `RF-015` y `CA-016`, que reproduce `H-01`; trasladar la condición de publicación al rango 3 o al rango 4 en esta spec, que excede su alcance de escritura y queda para una spec del régimen; mantener la delegación del `reviewer` sobre reportes publicados, que reproduce `H-02` sin corregir la matriz de permisos.

## Estrategia de testing

| Nivel | Instrumento | Resultado esperado |
|---|---|---|
| Unidad del cálculo del veredicto | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 4 veredictos y 4 precedencias acreditados, con el caso de 0 abiertos bajo `CONFORME` y el caso de 1 abierto de severidad `Alta` bajo `NO CONFORME` |
| Unidad de la compleción | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 82 identificadores frente a 82 filas con diferencia 0, y 1 error con la ruta y el identificador en el caso sintético con 1 fila retirada |
| Unidad de la regla citada | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 0 filas sin la forma `ruta §capítulo:línea` y 1 error en la fila sintética sin cita |
| Unidad del alcance de empaquetado | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 6 claves iguales en el rango 3 y el rango 4, y 1 error que nombra la clave ausente en el caso sintético de 5 claves |
| Unidad del destino del tag | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 2 filas T7 con el commit de merge en `main` y 1 error en la fila sintética que declara el commit de empaquetado |
| Unidad del cierre de los 16 | `python -m unittest tools.sdd.tests.test_hallazgos -q` | 11 filas en `cerrado` con evidencia de artefacto y 5 en `cerrado por ratificación` con identificador de commit |
| Integración del mecanismo | `python tools\sdd\validate.py --all` | Código de salida 0, 0 entradas `[ERROR]` y las comprobaciones nuevas dentro del alcance impreso |
| Agregado de la suite | `python -m unittest discover -s tools\sdd\tests -q` y `python -m unittest discover -s tools\git\tests -q` | 2 suites en `OK`, con las pruebas nuevas incluidas y sin regresión sobre las 187 y las 48 pruebas del corte |
| Compuerta | `python tools\sdd\validate.py --spec SPEC-016 --gate G2` | `OK: sin hallazgos.` y código de salida 0 |
| Revisión documental | Contraste manual de las 2 enumeraciones, de las 3 notas y de las 2 filas T7 | 2 conjuntos iguales, 3 notas sin línea retirada y 2 filas con el commit de merge como destino |

- El umbral de `RNF-003` se verifica con la ejecución agregada completa y su duración transcrita: 300 segundos o menos sobre el commit validado.
- La evidencia de las pruebas se transcribe en el campo `Evidencia` de la tarea que las ejecuta y no se declara antes de ejecutarse.

## Matriz de cobertura

| Requisito | Documento o componente | Verificación |
|---|---|---|
| `RF-001` | §16 del rango 3 y prohibiciones de la plantilla de `spec.md` | `test_autorreferencia` con 1 caso sintético que fija el veredicto y 1 spec publicada con su nota de regularización |
| `RF-002` | Notas de autorreferencia de `SPEC-013` y de `SPEC-015` y filas de motivo | `test_autorreferencia` exige la nota en el reporte y las 2 versiones resultantes de la tabla de `RF-002` |
| `RF-003` | Tabla de 6 artefactos de §15 y paso 3 del rango 4 | `test_seis_artefactos` compara los 2 conjuntos y nombra la diferencia |
| `RF-004` | Entrada `Unreleased` de `CHANGELOG.md` y acta de ratificación | `test_ratificacion` exige el identificador `564bac4`, las 3 rutas, el efecto declarativo y la firma del commit |
| `RF-005` | Nota del reporte de `SPEC-015` y bloque de la entrada `v0.7.1` | `test_registro_del_release` exige G5, G6 y el objeto del tag en los 2 soportes |
| `RF-006` | Filas T7 de `SPEC-014` y de `SPEC-015` | `test_destino_del_tag` exige el commit de merge, `main` y la ancestría, y rechaza el commit de empaquetado |
| `RF-007` | §12 del rango 3, plantilla del informe y `.opencode/agents/auditor.md` | `test_cauce_de_inventario` exige el cauce del `documenter` y la ausencia de la fila en el permiso del rol de auditoría |
| `RF-008` | Tabla de cierre de `RF-009` y evidencia de `AUD-106` y `AUD-107` | `test_cierre_de_los_dieciseis` exige el listado de ramas y la fila 35 del corpus con el resultado de la suite |
| `RF-009` | Tabla de cierre de las 11 observaciones | `test_cierre_de_los_dieciseis` exige 1 fila por observación y el estado cerrado solo con artefacto presente |
| `RF-010` | `test_historial_de_releases`, la constante de estados y la fila de `Unreleased` | `test_historial_de_releases` admite las filas de historial y de transición y el estado `released`, con el caso sintético del release sin fila |
| `RF-011` | `docs/sdd/inventario_hallazgos.md` y su fila en el corpus | `test_complecion` exige 82 filas para 82 identificadores, los 8 campos con contenido y la fila del documento en la tabla del corpus |
| `RF-012` | §16 del rango 3 y plantilla del informe con la regla citada | `test_regla_citada` exige la forma `ruta §capítulo:línea` y trata el juicio sin cita como observación |
| `RF-013` | Tabla de cálculo de §16 y anexo de observaciones | `test_veredicto` recorre las 4 condiciones y la precedencia, y detecta el veredicto que contradice el recuento |
| `RF-014` | `docs/sdd/ratificacion_historica.md` y las 5 filas de exención | `test_cierre_de_los_dieciseis` exige el estado `cerrado por ratificación` con identificador de commit firmado |
| `RF-015` | Validaciones de release del rango 4 y entrada del release `v0.7.2` | Contraste de la secuencia G5, auditoría y G6 y del efecto de un recuento de hallazgos abiertos distinto de 0 |
| `RF-016` | §12 del rango 3 y configuración del rol `reviewer` | Contraste de la autoría del `documenter` y de la firma del propietario sobre la nota de un reporte publicado, y del límite de escritura del `reviewer` a la spec en curso |
| `RF-017` | `MEMORY.md` y contraste con el frontmatter y con la fila del índice | Contraste del estado y del release pendiente en las 3 fuentes, con la cita del índice como fuente y la fila del historial de cambios |
| `RNF-001` | Requisitos, criterios y tareas de esta spec | `test_autorreferencia` recorre el contrato de la spec y devuelve 0 coincidencias |
| `RNF-002` | `SPEC-013`, `SPEC-014` y `SPEC-015` | Contraste de requisitos y criterios contra la versión anterior con 0 renumeraciones |
| `RNF-003` | Validación agregada | Duración transcrita de `python tools\sdd\validate.py --all` de 300 segundos o menos |
| `RNF-004` | Artefactos publicados modificados | `git show --no-patch --format=%G?` del commit de cada corrección publicada con firma verificable |
| `RNF-005` | Inventario de hallazgos | `test_complecion` exige 0 identificadores sin fila y 0 campos obligatorios vacíos |
| `RNF-006` | Inventario de hallazgos | `test_regla_citada` exige 0 filas sin cita por ruta, capítulo y línea |
| `RNF-007` | Informes de auditoría e inventario | `test_veredicto` exige 0 diferencias entre el veredicto declarado y el calculado |
| `RNF-008` | Acta de ratificación | `test_ratificacion` exige firma verificable y clave en la lista para cada violación histórica |
| `RNF-009` | Validaciones de release del rango 4 | Contraste de la auditoría previa sobre el estado integrado con 0 hallazgos abiertos |
| `CB-001` | Tabla de cierre de `RF-009` | `test_cierre_de_los_dieciseis` deja vigente la observación cuyo artefacto falta |
| `CB-002` | Acta de ratificación | `test_ratificacion` rechaza la ratificación con estado de firma distinto de `G` |
| `CB-003` | §15 del rango 3 y paso 3 del rango 4 | `test_seis_artefactos` produce 1 error que nombra la diferencia y no declara alineada la enumeración |
| `CB-004` | Filas T7 de `SPEC-014` y de `SPEC-015` | `test_destino_del_tag` rechaza la corrección que altera el destino, el campo `release` o el identificador |
| `CB-005` | Reporte de `SPEC-015` | `test_registro_del_release` conserva la transcripción previa y añade la nota a continuación |
| `CB-006` | §16 del rango 3 y G1 | `test_autorreferencia` registra el hallazgo y el requisito queda sin aprobación |
| `CB-007` | §12 del rango 3 y comprobación de inventario | `test_cauce_de_inventario` deja el check en rojo con la ruta del informe sin fila |
| `CB-008` | Inventario de hallazgos | `test_complecion` registra el estado nuevo sobre el identificador existente sin asignar otro |
| `CB-009` | Análisis del informe y anexo de observaciones | `test_regla_citada` excluye la observación del recuento de hallazgos |
| `CB-010` | Cálculo del veredicto | `test_veredicto` registra el error con la fila que sostiene la diferencia |
| `CB-011` | Acta de ratificación | `test_ratificacion` exige alcance y efecto declarados y 0 líneas retiradas del contenido publicado |
| `CB-012` | Validaciones de release del rango 4 | Contraste del veredicto distinto de `CONFORME` con la retención de la spec en `validated` |
| `CB-013` | Compleción del inventario | `test_complecion` deja el check en rojo con la ruta del informe sin fila |

## Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Una fila del inventario sin regla citada en el informe de origen | El recuento de `RNF-006` no llega a 0 y el cierre se detiene | La fila transcribe la norma que el informe cita en su propia evidencia; si el informe no la cita, el juicio consta en el anexo de observaciones y la comprobación nombra el identificador |
| El acta de ratificación se introduce en un commit sin firma verificable | Las 5 filas no alcanzan `cerrado por ratificación` y el veredicto queda en `PARCIAL` | `CB-002` se verifica antes de cerrar `T-028` y la evidencia transcribe el estado de firma y la huella de la clave |
| La corrección de una fila T7 altera el campo `release` | Se pierde la trazabilidad del release publicado | `CB-004` compara el destino, el campo `release` y el identificador antes y después de la corrección y rechaza el cambio |
| La comprobación de autorreferencia marca un requisito que define el cálculo | Falso positivo sobre esta spec | La detección exige una referencia concreta y una salida fijada, y la prueba negativa se ejecuta sobre el contrato de esta spec |
| La integración de un informe de auditoría deja el corpus con un archivo sin fila | El check `verify` queda en rojo y la integración se detiene | La fila del corpus y la fila de cada hallazgo se escriben antes de la integración, y la comprobación nombra la ruta ausente |
